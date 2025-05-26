# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    asset = models.PositiveIntegerField(default=0)        # 기존 보유 자산
    salary = models.PositiveIntegerField(default=0)
    age = models.PositiveIntegerField(default=0)
    saving_type = models.CharField(max_length=20, blank=True)
    invest_type = models.CharField(max_length=20, blank=True)
    main_bank = models.CharField(max_length=50, blank=True)
    
    investment_amount = models.PositiveIntegerField(default=0)  # 신규 투자 금액 필드 추가

    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        related_query_name='follower',
        blank=True
    )

User = get_user_model()

class FavoriteStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_stocks')
    symbol = models.CharField(max_length=10)  # 예: AAPL
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'symbol')
