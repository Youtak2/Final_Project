<template>
  <div class="auth-container">
    <h2>로그인</h2>

    <!-- 일반 로그인 -->
    <RouterLink to="/login" class="btn primary">로그인</RouterLink>
    <RouterLink to="/signup" class="btn">회원가입</RouterLink>

    <hr />

    <!-- 소셜 로그인 -->
<button class="social kakao" @click="kakaoLogin">카카오 로그인</button>
<button class="social naver" @click="naverLogin">네이버 로그인</button>
<button class="social google" @click="googleLogin">Google 계정으로 로그인</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// ✅ 인가 코드 방식: 카카오 로그인
const kakaoLogin = () => {
  const REST_API_KEY = '9a9661d3363caf49aa0f1613461b76e6'
  const REDIRECT_URI = 'http://localhost:5173/oauth/kakao'

  const kakaoAuthUrl =
    `https://kauth.kakao.com/oauth/authorize?` +
    `client_id=${REST_API_KEY}` +
    `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
    `&response_type=code` +
    `&prompt=login` // 👈 계정선택 매번 유도

  // ✅ 실제 이동 추가
  window.location.href = kakaoAuthUrl
}

// ✅ 기존 구글 로그인 유지
const googleLogin = () => {
  const clientId = '854189614623-n676v9ug587tlri6scmhmbrjss7q0vqe.apps.googleusercontent.com'
  const redirectUri = 'http://localhost:5173/oauth/google'
  const scope = 'openid email profile'

  const googleAuthUrl =
    `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&response_type=token&scope=${encodeURIComponent(scope)}` +
    `&prompt=consent`

  window.location.href = googleAuthUrl
}
const naverLogin = () => {
  const clientId = '9FnwMn7AkGM2D9KTbEVZ' // ← 네 네이버 앱의 Client ID
  const redirectUri = 'http://localhost:5173/oauth/naver'
  const state = crypto.randomUUID() // CSRF 방지

  const naverAuthUrl =
    `https://nid.naver.com/oauth2.0/authorize?response_type=code` +
    `&client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&state=${state}` +
    `&auth_type=reauthenticate`  // ✅ 매번 계정 선택하게 함

  window.location.href = naverAuthUrl
}

</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.btn {
  display: block;
  width: 100%;
  margin: 0.5rem 0;
  padding: 0.8rem;
  font-weight: bold;
  border: 1px solid #ccc;
  border-radius: 6px;
  text-decoration: none;
  color: #333;
}

.btn.primary {
  background-color: #333;
  color: white;
  border: none;
}

.find-account {
  margin-top: 1rem;
  font-size: 0.85rem;
  text-decoration: underline;
  color: #555;
  cursor: pointer;
}

.social {
  width: 100%;
  padding: 0.8rem;
  margin: 0.4rem 0;
  border-radius: 6px;
  font-weight: bold;
  border: none;
  cursor: pointer;
}

.kakao {
  background-color: #fee500;
}

.naver {
  background-color: #03c75a;
  color: white;
}

.google-btn {
  margin-top: 0.4rem;
  display: flex;
  justify-content: center;
}
</style>
