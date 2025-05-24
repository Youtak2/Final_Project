import yfinance as yf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def get_financials(request):
    symbol = request.GET.get('symbol')
    f_type = request.GET.get('type')

    ticker = yf.Ticker(symbol)

    try:
        if f_type == 'income':
            data = ticker.financials
        elif f_type == 'balance':
            data = ticker.balance_sheet
        elif f_type == 'cashflow':
            data = ticker.cashflow
        else:
            return Response({'error': 'Invalid type'}, status=400)

        if data is None or data.empty:
            return Response({'error': 'No data found'}, status=404)

        # ✅ 열 이름을 문자열로 변환
        data.columns = data.columns.astype(str)

        return Response(data.fillna("").to_dict())

    except Exception as e:
        return Response({'error': str(e)}, status=500)

