"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('dj_rest_auth.urls')),                     # 로그인, 로그아웃
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('api/v1/accounts/', include('accounts.urls')),                     # check-username, signup
    path('api/v1/community/',include('community.urls')),
    path('api/v1/deposit/', include('deposit.urls')),                       # 예적금 금리비교
    path('api/v1/financial/', include('financial.urls')),                   # 관심 종목 정보 검색
    path('api/v1/stock/',include('stock.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/recommend/', include('recommend.urls')),
    path('api/v1/simulation/', include('simulation.urls')),
]