from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404

from .serializers import CustomUserDetailsSerializer


User = get_user_model()

# ✅ 아이디 중복 확인
@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request):
    username = request.GET.get('username')
    if not username:
        return Response({'available': False})
    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})

# ✅ 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    name = request.data.get('name')
    email = request.data.get('email')

    if password != password2:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=name,
        email=email
    )
    return Response({'message': '회원가입 성공!'}, status=status.HTTP_201_CREATED)

# ✅ 로그인 (토큰 발급)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ 사용자 정보 수정
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.email = request.data.get('email', user.email)
    asset = request.data.get('asset')
    salary = request.data.get('salary')
    age = request.data.get('age')

    if asset is not None:
        user.asset = asset
    if salary is not None:
        user.salary = salary
    if age is not None:
        user.age = age

    user.save()
    return Response({'message': '유저 정보 수정 완료'})

# ✅ 포트폴리오 정보 조회 & 수정
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_portfolio(request):
    user = request.user

    if request.method == 'GET':
        # ✅ 현재 사용자 정보 반환
        return Response({
            'saving_type': user.saving_type,
            'invest_type': user.invest_type,
            'main_bank': user.main_bank
        })

    elif request.method == 'PATCH':
        print('📦 받은 데이터:', request.data)
        serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '포트폴리오 업데이트 완료'})
        print('❌ serializer error:', serializer.errors)
        return Response(serializer.errors, status=400)