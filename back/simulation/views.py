from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
from django.db import transaction
import yfinance as yf

from .models import Portfolio, Holding, Transaction
from .serializers import PortfolioSerializer, TransactionSerializer

def fetch_latest_price(symbol):
    ticker = yf.Ticker(symbol)
    try:
        hist = ticker.history(period="1d")
        if hist.empty or 'Close' not in hist or len(hist['Close']) == 0:
            return None
        return Decimal(hist['Close'][-1])
    except Exception:
        return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_view(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    serializer = PortfolioSerializer(portfolio)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_stock(request):
    symbol = request.data.get('symbol')
    shares = request.data.get('shares')

    if not symbol or shares is None:
        return Response({"error": "symbol and shares are required"}, status=400)

    if not isinstance(symbol, str):
        return Response({"error": "invalid symbol format"}, status=400)
    symbol = symbol.upper()

    try:
        shares = Decimal(shares)
    except (ValueError, TypeError, InvalidOperation):
        return Response({"error": "invalid shares value"}, status=400)

    if shares <= 0 or shares != shares.to_integral_value():
        return Response({"error": "shares must be a positive integer"}, status=400)

    price = fetch_latest_price(symbol)
    if price is None:
        return Response({"error": "Failed to fetch price"}, status=400)

    cost = price * shares

    with transaction.atomic():
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)

        if portfolio.cash_balance < cost:
            return Response({"error": "Insufficient cash balance"}, status=400)

        holding, created = Holding.objects.get_or_create(
            portfolio=portfolio, symbol=symbol, defaults={'shares': 0, 'avg_price': Decimal('0')}
        )

        total_shares = holding.shares + shares
        total_cost = holding.avg_price * holding.shares + cost
        new_avg_price = total_cost / total_shares

        holding.shares = total_shares
        holding.avg_price = new_avg_price
        holding.save()

        portfolio.cash_balance -= cost
        portfolio.save()

        Transaction.objects.create(
            portfolio=portfolio,
            symbol=symbol,
            shares=shares,
            price=price,
            transaction_type=Transaction.BUY
        )

    return Response({"message": f"Bought {shares} shares of {symbol} at {price} USD"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_stock(request):
    symbol = request.data.get('symbol')
    shares = request.data.get('shares')

    if not symbol or shares is None:
        return Response({"error": "symbol and shares are required"}, status=400)

    if not isinstance(symbol, str):
        return Response({"error": "invalid symbol format"}, status=400)
    symbol = symbol.upper()

    try:
        shares = Decimal(shares)
    except (ValueError, TypeError, InvalidOperation):
        return Response({"error": "invalid shares value"}, status=400)

    if shares <= 0 or shares != shares.to_integral_value():
        return Response({"error": "shares must be a positive integer"}, status=400)

    with transaction.atomic():
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)

        try:
            holding = Holding.objects.get(portfolio=portfolio, symbol=symbol)
        except Holding.DoesNotExist:
            return Response({"error": "You do not own this stock"}, status=400)

        if holding.shares < shares:
            return Response({"error": "Insufficient shares to sell"}, status=400)

        price = fetch_latest_price(symbol)
        if price is None:
            return Response({"error": "Failed to fetch price"}, status=400)

        holding.shares -= shares
        if holding.shares == 0:
            holding.delete()
        else:
            holding.save()

        revenue = price * shares
        portfolio.cash_balance += revenue
        portfolio.save()

        Transaction.objects.create(
            portfolio=portfolio,
            symbol=symbol,
            shares=shares,
            price=price,
            transaction_type=Transaction.SELL
        )

    return Response({"message": f"Sold {shares} shares of {symbol} at {price} USD"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_current_prices(request):
    symbols = request.data.get('symbols', [])
    result = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.info['regularMarketPrice']
            result[symbol] = round(price, 2)
        except:
            result[symbol] = None

    return Response(result)