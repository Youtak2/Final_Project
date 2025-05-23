from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    def get_replies(self, obj):
        # 대댓글이 있을 경우 재귀적으로 serialize
        return CommentSerializer(obj.replies.all(), many=True).data

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies', 'parent']
        extra_kwargs = {'parent': {'required': False}}
class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    liked_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_following = serializers.SerializerMethodField()  # ✅ 추가

    def get_user(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = Article
        fields = ['id', 'user', 'title', 'content', 'created_at', 'liked_users', 'is_following']
