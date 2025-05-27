from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings  # ✅ settings에서 불러오기
from .models import FavoriteStock
from .serializers import CustomUserDetailsSerializer, FavoriteStockSerializer

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
import requests
import json

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request):
    username = request.GET.get('username')
    if not username:
        return Response({'available': False})
    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})

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

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    user.first_name = request.data.get('first_name', user.first_name)
    user.email = request.data.get('email', user.email)
    asset = request.data.get('asset')
    salary = request.data.get('salary')
    age = request.data.get('age')
    investment_amount = request.data.get('investment_amount')

    if asset is not None:
        user.asset = asset
    if salary is not None:
        user.salary = salary
    if age is not None:
        user.age = age
    if investment_amount is not None:
        user.investment_amount = investment_amount

    user.save()
    return Response({'message': '유저 정보 수정 완료'})

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_portfolio(request):
    user = request.user

    if request.method == 'GET':
        return Response({
            'saving_type': user.saving_type,
            'invest_type': user.invest_type,
            'main_bank': user.main_bank,
            'investment_amount': getattr(user, 'investment_amount', 0)
        })

    elif request.method == 'PATCH':
        serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            investment_amount = request.data.get('investment_amount')
            if investment_amount is not None:
                try:
                    user.investment_amount = int(investment_amount)
                    user.save()
                except Exception as e:
                    return Response({"investment_amount": "유효하지 않은 값입니다."}, status=400)
            return Response({'message': '포트폴리오 업데이트 완료'})
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_stocks(request):
    user = request.user

    if request.method == 'GET':
        favorites = FavoriteStock.objects.filter(user=user)
        serializer = FavoriteStockSerializer(favorites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        symbol = request.data.get('symbol')
        if not symbol:
            return Response({'error': 'symbol is required'}, status=400)
        fav, created = FavoriteStock.objects.get_or_create(user=user, symbol=symbol)
        return Response({'message': '관심 종목 등록 완료' if created else '이미 등록됨'})

    elif request.method == 'DELETE':
        symbol = request.data.get('symbol')
        FavoriteStock.objects.filter(user=user, symbol=symbol).delete()
        return Response({'message': '삭제 완료'})

    return Response({'error': '잘못된 요청입니다.'}, status=405)

@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login(request):
    code = request.data.get('code')
    redirect_uri = request.data.get('redirect_uri')

    if not code or not redirect_uri:
        return Response({'error': 'code와 redirect_uri가 필요합니다.'}, status=400)

    REST_API_KEY = settings.KAKAO_REST_API_KEY

    token_url = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': REST_API_KEY,
        'redirect_uri': redirect_uri,
        'code': code
    }

    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return Response({'error': 'access_token 발급 실패', 'detail': token_json}, status=400)

    profile_response = requests.get(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    profile_json = profile_response.json()
    kakao_id = profile_json.get('id')
    nickname = profile_json.get('properties', {}).get('nickname', '')

    if not kakao_id:
        return Response({'error': '사용자 정보 조회 실패'}, status=400)

    username = f'kakao_{kakao_id}'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.first_name = nickname
        user.set_unusable_password()
        user.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    serializer = CustomUserDetailsSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def naver_login(request):
    code = request.data.get('code')
    state = request.data.get('state')
    redirect_uri = request.data.get('redirect_uri')

    if not code or not state or not redirect_uri:
        return Response({'error': 'code, state, redirect_uri 필요'}, status=400)

    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET

    token_url = 'https://nid.naver.com/oauth2.0/token'
    params = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'state': state,
    }
    res = requests.get(token_url, params=params)
    token_json = res.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return Response({'error': 'access_token 발급 실패', 'detail': token_json}, status=400)

    profile = requests.get(
        'https://openapi.naver.com/v1/nid/me',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    try:
        naver_id = profile['response']['id']
        nickname = profile['response'].get('nickname', '')
    except KeyError:
        return Response({'error': '사용자 정보 조회 실패'}, status=400)

    username = f'naver_{naver_id}'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.first_name = nickname
        user.set_unusable_password()
        user.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response):
        if not response:
            return Response({"error": "응답이 비어있습니다."}, status=400)
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                return Response({"error": "응답 파싱 실패"}, status=400)
        if "id_token" not in response:
            return Response({"error": "id_token이 응답에 없습니다."}, status=400)
        sociallogin = self.get_social_login(request, app, response)
        if sociallogin.is_existing:
            return Response({"error": "이미 존재하는 사용자입니다."}, status=400)
        sociallogin.save(request)
        return super().complete_login(request, app, token, response)

class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
