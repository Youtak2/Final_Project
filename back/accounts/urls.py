from django.urls import path
from .views import GoogleLogin
from . import views
from .views import naver_login
urlpatterns = [
    path('check-username/', views.check_username),
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('update/', views.update_user),
    path('portfolio/', views.update_portfolio),  # ✅ 수정 완료
    path('favorites/', views.favorite_stocks),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),

    # 카카오 소셜 로그인 클래스뷰로 변경
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('user/', views.user_info),  # ✅ 이 줄 추가
    path('naver/login/', naver_login),  # ✅ 추가
]