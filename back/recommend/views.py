from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pandas as pd
import joblib
import os
import numpy as np
from django.db import transaction
from .ml_model.quant_score import calculate_quant_score
from .models import RecommendedStock
from deposit.models import DepositProduct
from .serializers import RecommendedStockSerializer  # Serializer 임포트 필요

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'ml_model', 'training_data_cleaned.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'ml_model', 'model.pkl')
model = joblib.load(MODEL_PATH)


def make_reason_ml(roe, rsi, sma_diff, per, probability):
    reasons = []
    if roe is not None and roe > 0.1:
        reasons.append(f"ROE가 {roe:.1%}로 높습니다.")
    if rsi is not None:
        if rsi > 70:
            reasons.append(f"RSI가 {rsi:.0f}로 과매수 상태입니다.")
        elif rsi < 30:
            reasons.append(f"RSI가 {rsi:.0f}로 과매도 상태입니다.")
        else:
            reasons.append(f"RSI가 {rsi:.0f}로 중립입니다.")
    if sma_diff is not None and sma_diff > 0:
        reasons.append("현재 주가가 이동평균선보다 높습니다.")
    if per is not None and per < 20:
        reasons.append(f"PER이 {per:.1f}로 저평가 구간일 수 있습니다.")
    return " ".join(reasons)


def safe_feature_input(row):
    try:
        features = row[['PER', 'ROE', 'SMA20_diff', 'RSI']]
        features = features.replace([np.inf, -np.inf], np.nan)
        features = features.infer_objects(copy=False)
        features = features.apply(lambda x: np.nan if abs(x) > 1e6 else x)
        if features.isnull().any() or not np.isfinite(features).all():
            return None
        return pd.DataFrame([features], columns=features.index).astype('float32')
    except Exception as e:
        print(f"⚠️ feature 처리 오류: {e}")
        return None


def recommend_savings(saving_type):
    if saving_type == '소극적':
        target_term = 36
    elif saving_type == '적극적':
        target_term = 6
    else:
        target_term = 12

    products = DepositProduct.objects.filter(save_term=target_term).order_by('-rate')[:6]

    result = []
    for p in products:
        result.append({
            '금융회사': p.bank_name,
            '상품명': p.name,
            '추천_금리': round(p.rate, 2),
            '저축기간': p.save_term,
            '가입링크': p.join_url or '',
        })
    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_stocks(request):
    user = request.user
    invest_type = getattr(user, 'invest_type', None)
    saving_type = getattr(user, 'saving_type', None)
    investment_amount = getattr(user, 'investment_amount', 0)

    if not invest_type:
        return Response({"error": "투자 성향을 설정해주세요.", "redirect": "/mypage/portfolio"}, status=400)
    if not saving_type:
        return Response({"error": "저축 성향을 설정해주세요.", "redirect": "/mypage/portfolio"}, status=400)

    is_vip = investment_amount >= 100000000  # 1억 이상이면 VIP

    # 1. 캐시된 추천이 있는지 확인
    saved_recommendations = RecommendedStock.objects.filter(user=user, invest_type=invest_type).order_by('-probability')[:20]

    if saved_recommendations.exists():
        serializer = RecommendedStockSerializer(saved_recommendations, many=True)
        average_prediction_rate = round(np.mean([rec.probability for rec in saved_recommendations]), 4)
        saving_recommendations = recommend_savings(saving_type)
        return Response({
            "stock_recommendations": serializer.data,
            "average_prediction_rate": average_prediction_rate,
            "saving_recommendations": saving_recommendations,
            "is_vip": is_vip,
            "from_cache": True,
        })

    # 2. 캐시 없으면 ML 계산 수행
    weight_map = {
        '안정형': (0.4, 0.6),
        '위험중립형': (0.6, 0.4),
        '공격투자형': (0.8, 0.2)
    }
    ml_weight, quant_weight = weight_map.get(invest_type, (0.6, 0.4))

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        return Response({"error": "CSV 파일을 읽을 수 없습니다."}, status=500)

    results = []
    for idx, row in df.iterrows():
        X = safe_feature_input(row)
        if X is None:
            continue
        ml_prob = model.predict_proba(X)[0][1]
        quant_score = calculate_quant_score(row)
        final_score = ml_weight * ml_prob + quant_weight * (quant_score / 4)
        reason = make_reason_ml(row['ROE'], row['RSI'], row['SMA20_diff'], row['PER'], ml_prob)

        results.append({
            'symbol': row['symbol'],
            'PER': row['PER'],
            'ROE': row['ROE'],
            'RSI': row['RSI'],
            'probability': round(final_score, 4),
            'reason': reason,
            'invest_type': invest_type
        })

    top20 = sorted(results, key=lambda x: -x['probability'])[:20]

    try:
        with transaction.atomic():
            RecommendedStock.objects.filter(user=user).delete()
            objs = [
                RecommendedStock(
                    user=user,
                    symbol=s['symbol'],
                    per=s['PER'],
                    roe=s['ROE'],
                    rsi=s['RSI'],
                    probability=s['probability'],
                    reason=s['reason'],
                    invest_type=s['invest_type']
                ) for s in top20
            ]
            RecommendedStock.objects.bulk_create(objs)
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")

    average_prediction_rate = round(np.mean([r['probability'] for r in results]), 4) if results else 0
    saving_recommendations = recommend_savings(saving_type)

    return Response({
        "stock_recommendations": top20,
        "average_prediction_rate": average_prediction_rate,
        "saving_recommendations": saving_recommendations,
        "is_vip": is_vip,
        "from_cache": False,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_savings_api(request):
    user = request.user
    saving_type = getattr(user, 'saving_type', None)
    if not saving_type:
        return Response({"error": "저축 성향을 설정해주세요.", "redirect": "/mypage/portfolio"}, status=400)
    recommendations = recommend_savings(saving_type)
    return Response(recommendations)

