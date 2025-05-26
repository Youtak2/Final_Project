from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/create/', views.create_article),
    path('articles/<int:article_id>/', views.article_detail),
    path('articles/<int:article_id>/edit/', views.article_update_delete),
    path('articles/<int:article_id>/comments/', views.article_comments),
    path('articles/<int:article_id>/comments/create/', views.create_comment),
    path('articles/<int:article_id>/like/', views.toggle_like),
    path('users/<int:user_id>/follow/', views.toggle_follow),  # ✅ 수정된 부분
    path('users/<int:user_id>/followings/', views.get_followings),  # ✅ 팔로우 목록
    path('users/<int:user_id>/activity/', views.user_articles_comments),  # ✅ 작성자 활동
    path('comments/<int:comment_id>/like/', views.toggle_comment_like),
    path('users/<int:user_id>/followers/', views.get_followers),
]