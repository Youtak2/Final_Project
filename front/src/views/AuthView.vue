<template>
  <div class="auth-container">
    <h2>로그인</h2>

    <!-- 일반 로그인 -->
    <RouterLink to="/login" class="btn primary">로그인</RouterLink>
    <RouterLink to="/signup" class="btn">회원가입</RouterLink>

    <hr />

    <!-- 소셜 로그인 -->
    <button class="social kakao" @click="kakaoLogin">카카오 로그인</button>
    <button class="social naver">네이버 로그인</button>
    <div id="google-btn" class="google-btn"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VueJwtDecode from 'vue-jwt-decode'

const router = useRouter()

const kakaoLogin = () => {
  const REST_API_KEY = '당신의_카카오_REST_API_KEY'
  const REDIRECT_URI = 'http://localhost:5173/oauth/kakao'
  window.location.href =
    `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`
}

const handleGoogleLogin = (res) => {
  const user = VueJwtDecode.decode(res.credential)
  console.log('✅ Google 로그인 완료:', user)
  localStorage.setItem('token', 'mock-token') // 실제는 백엔드 연동 필요
  router.push('/')
}

onMounted(() => {
  const google = window.google
  if (google) {
    google.accounts.id.initialize({
      client_id: '당신의_GOOGLE_CLIENT_ID',
      callback: handleGoogleLogin
    })
    google.accounts.id.renderButton(
      document.getElementById('google-btn'),
      { theme: 'outline', size: 'large' }
    )
  }
})
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
