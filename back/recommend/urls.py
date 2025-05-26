from django.urls import path
from .views import recommend_stocks, recommend_savings_api  # 뷰 함수명 확인

urlpatterns = [
    path('', recommend_stocks),
    path('savings/', recommend_savings_api, name='recommend_savings'),  # API 뷰 함수 등록
]
