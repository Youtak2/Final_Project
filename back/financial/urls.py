# stocks/urls.py
from django.urls import path
from .views import get_financials

urlpatterns = [
    path('financials/', get_financials),
]
