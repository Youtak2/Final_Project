from rest_framework import serializers
from .models import Portfolio, Holding, Transaction

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['symbol', 'shares', 'avg_price']

class PortfolioSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)  # read_only 권장

    class Meta:
        model = Portfolio
        fields = ['cash_balance', 'holdings']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['symbol', 'shares', 'price', 'transaction_type', 'timestamp']
        read_only_fields = ['timestamp']
