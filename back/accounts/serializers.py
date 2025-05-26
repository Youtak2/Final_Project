from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from .models import FavoriteStock
from rest_framework import serializers

User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'username', 'email', 'asset', 'salary', 'age',
            'saving_type', 'invest_type', 'main_bank', 'investment_amount'  # <== 추가
        )

class FavoriteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteStock
        fields = ['id', 'symbol', 'added_at']
