# stock/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .utils import get_yahoo_price_data, save_to_db
from .models import PriceData
from .serializers import PriceDataSerializer
from datetime import timedelta, date


@api_view(['GET'])
@permission_classes([AllowAny])
def stock_price_view(request):
    ticker = request.GET.get('ticker')
    range_type = request.GET.get('range', '1d')

    if not ticker:
        return Response({'error': 'ticker 쿼리 파라미터는 필수입니다.'}, status=400)

    days_map = {
        '1d': 1,
        '1w': 7,
        '1m': 30,
        '3m': 90,
        '1y': 365,
    }
    days = days_map.get(range_type, 1)

    df = get_yahoo_price_data(ticker, days=days)
    if df.empty:
        return Response({'error': '시세 데이터를 가져올 수 없습니다.'}, status=404)

    save_to_db(df, ticker)

    queryset = PriceData.objects.filter(
        ticker=ticker,
        date__gte=date.today() - timedelta(days=days)
    ).order_by('date')

    serializer = PriceDataSerializer(queryset, many=True)
    return Response({'prices': serializer.data})  # ← 이 부분 수정

