from django.db import models
from django.contrib.auth import get_user_model

class DepositProduct(models.Model):
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=10)  # 예금 / 적금
    save_term = models.IntegerField()               # 6 / 12 / 24 / 36 (개월)
    rate = models.FloatField()
    fin_prdt_cd = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)   # 상품 상세 설명 
    join_url = models.URLField(blank=True, null=True)   # 가입 링크
    join_way = models.TextField(blank=True, null=True)  # 가입 경로
    join_member = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # 한 유저가 동일 상품을 중복 찜 못 하도록