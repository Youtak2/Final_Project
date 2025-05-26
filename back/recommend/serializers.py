# recommend/serializers.py
from rest_framework import serializers
from .models import RecommendedStock

class RecommendedStockSerializer(serializers.ModelSerializer):
    PER = serializers.FloatField(source='per')
    ROE = serializers.FloatField(source='roe')
    RSI = serializers.FloatField(source='rsi')
    probability = serializers.FloatField()   # 추가

    class Meta:
        model = RecommendedStock
        fields = ['symbol', 'PER', 'ROE', 'RSI', 'probability', 'reason']  # probability 포함
