from django.urls import path
from .views import stock_price_view

urlpatterns = [
    path('', stock_price_view),
]
