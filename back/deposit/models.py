from django.db import models

class DepositProduct(models.Model):
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=10)  # 예금 / 적금
    save_term = models.IntegerField()               # 6 / 12 / 24 / 36 (개월)
    rate = models.FloatField()
    fin_prdt_cd = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


