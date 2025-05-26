from django.db import models
from django.conf import settings
from decimal import Decimal

class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('100000.00'))

    def __str__(self):
        return f"{self.user.username} Portfolio"

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    symbol = models.CharField(max_length=10)
    shares = models.DecimalField(max_digits=20, decimal_places=4)
    avg_price = models.DecimalField(max_digits=15, decimal_places=4)

    class Meta:
        unique_together = ('portfolio', 'symbol')

    def __str__(self):
        return f"{self.symbol} - {self.shares} shares"

class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TRANSACTION_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    symbol = models.CharField(max_length=10)
    shares = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.shares} {self.symbol} at {self.price}"
