from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
User = get_user_model()
@api_view(['GET'])  # ✅ 반드시 GET만 받도록 지정
def check_username(request):
    username = request.GET.get('username')
    if not username:
        return Response({'available': False})
    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2')
    name = request.data.get('name')
    email = request.data.get('email')  # ✅ 추가

    if password != password2:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ email과 name 포함해서 저장
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=name,
        email=email
    )
    return Response({'message': '회원가입 성공!'}, status=status.HTTP_201_CREATED)

def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)
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
