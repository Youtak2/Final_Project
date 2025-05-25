# recommend/urls.py
from django.urls import path
from .views import recommend_stocks

urlpatterns = [
    path('', recommend_stocks),
]
