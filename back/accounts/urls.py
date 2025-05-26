from django.urls import path
from . import views

urlpatterns = [
    path('check-username/', views.check_username),
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('update/', views.update_user),
    path('portfolio/', views.update_portfolio),  # ✅ 수정 완료
    path('favorites/', views.favorite_stocks),
]