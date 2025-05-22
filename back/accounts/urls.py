from django.urls import path
from . import views

urlpatterns = [
    path('check-username/', views.check_username),
    path('signup/', views.signup),  # ✅ 이 줄 추가
    path('login/', views.login_view),
    path('update/', views.update_user),
    
    
]