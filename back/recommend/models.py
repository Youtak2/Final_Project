# recommend/models.py
from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

User = get_user_model()
class RecommendedStock(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    per = models.FloatField(null=True, blank=True)
    roe = models.FloatField(null=True, blank=True)
    rsi = models.FloatField(null=True, blank=True)
    probability = models.FloatField(default=0.0)
    reason = models.TextField()
    invest_type = models.CharField(max_length=20, null=True, blank=True)  # ✅ 반드시 필요
    created_at = models.DateTimeField(auto_now_add=True)
    