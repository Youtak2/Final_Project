from django.urls import path
from .views import DepositProductListView

urlpatterns = [
    path('products/', DepositProductListView.as_view(), name='deposit-products'),
]
