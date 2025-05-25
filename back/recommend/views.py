from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pandas as pd
import joblib
import os
from .ml_model.quant_score import calculate_quant_score

# 모델 및 데이터 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'ml_model', 'training_data_cleaned.csv')
model = joblib.load(os.path.join(BASE_DIR, 'ml_model', 'model.pkl'))


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_stocks(request):
    user = request.user

    try:
        invest_type = user.invest_type  # CustomUser에 직접 존재
    except Exception:
        invest_type = '위험중립형'

    weight_map = {
        '안정형': (0.4, 0.6),
        '위험중립형': (0.6, 0.4),
        '공격투자형': (0.8, 0.2)
    }
    ml_weight, quant_weight = weight_map.get(invest_type, (0.6, 0.4))

    df = pd.read_csv(CSV_PATH)
    results = []

    for _, row in df.iterrows():
        symbol = row['symbol']
        try:
            features = row[['PER', 'ROE', 'SMA20_diff', 'RSI']]\
                .replace([float('inf'), float('-inf')], pd.NA)\
                .infer_objects(copy=False)

            if features.isnull().any():
                continue

            X = pd.DataFrame([features.to_list()], columns=features.index).astype('float32')
            ml_prob = model.predict_proba(X)[0][1]
            quant_score = calculate_quant_score(row)
            final_score = ml_weight * ml_prob + quant_weight * (quant_score / 4)

            results.append({
                'symbol': symbol,
                'PER': row['PER'],
                'ROE': row['ROE'],
                'RSI': row['RSI'],
                'probability': round(final_score, 4),
                'reason': make_reason_ml(row['ROE'], row['RSI'], row['SMA20_diff'], row['PER'], ml_prob)
            })

            print(f"✅ {symbol} 예측 성공. 확률={final_score:.4f}")

        except Exception as e:
            print(f"⚠️ {symbol} 예측 실패: {e}")
            continue

    top20 = sorted(results, key=lambda x: -x['probability'])[:20]

    return Response({
        "invest_type": invest_type,
        "total_evaluated": len(results),
        "top_20": top20
    })
