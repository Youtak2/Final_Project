from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

User = get_user_model()

# ✅ 누구나 조회 가능
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

# ✅ 로그인한 사용자만 작성 가능
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    # ✅ request를 context로 명시적으로 전달해야 is_following 동작함
    serializer = ArticleSerializer(article, context={'request': request})
    return Response(serializer.data)


# ✅ 로그인한 사용자만 수정/삭제 가능
@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def article_update_delete(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=204)

# ✅ 누구나 댓글 목록 조회 가능
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def article_comments(request, article_id):
    comments = Comment.objects.filter(article_id=article_id, parent=None)  # ✅ 최상위 댓글만 조회
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# ✅ 로그인한 사용자만 댓글 작성 가능
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment(request, article_id):
    article = Article.objects.get(pk=article_id)
    parent_id = request.data.get('parent')
    parent = Comment.objects.get(pk=parent_id) if parent_id else None
    comment = Comment.objects.create(
        article=article,
        user=request.user,
        content=request.data['content'],
        parent=parent
    )
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=201)

# ✅ 로그인한 사용자만 좋아요 가능
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, article_id):
    article = Article.objects.get(pk=article_id)
    user = request.user
    if user in article.liked_users.all():
        article.liked_users.remove(user)
        return Response({'detail': '좋아요 취소'})
    else:
        article.liked_users.add(user)
        return Response({'detail': '좋아요 완료'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_follow(request, user_id):
    try:
        if request.user.id == user_id:
            return Response({'detail': '본인은 팔로우할 수 없습니다.'}, status=400)

        target = User.objects.get(pk=user_id)
        if request.user.followings.filter(pk=target.pk).exists():
            request.user.followings.remove(target)
            print(f"[언팔로우] {request.user.username} → {target.username}")
            return Response({'detail': '언팔로우 완료'})
        else:
            request.user.followings.add(target)
            print(f"[팔로우] {request.user.username} → {target.username}")
            return Response({'detail': '팔로우 완료'})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=500)


# ✅ 팔로우 목록 조회
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_followings(request, user_id):
    user = User.objects.get(pk=user_id)
    followings = user.followings.all()
    data = [{'id': u.id, 'username': u.username} for u in followings]
    return Response(data)


# ✅ 작성자 게시글 + 댓글 보기
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_articles_comments(request, user_id):
    user = User.objects.get(pk=user_id)
    articles = Article.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    return Response({
        'articles': ArticleSerializer(articles, many=True).data,
        'comments': CommentSerializer(comments, many=True).data,
    })