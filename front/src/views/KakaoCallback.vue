<template>
  <div>
    <p>카카오 로그인 처리 중...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'  // ✅ Pinia store import

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()  // ✅ store instance

onMounted(async () => {
  const code = route.query.code
  if (!code) {
    alert('인가 코드가 없습니다.')
    router.push('/login')
    return
  }

  try {
    // 🔐 백엔드에 인가 코드 보내서 토큰 발급
    const res = await axios.post('http://localhost:8000/api/v1/accounts/kakao/login/', {
      code,
      redirect_uri: 'http://localhost:5173/oauth/kakao'
    })

    const token = res.data.token || res.data.key
    auth.setToken(token)         // ✅ Pinia store에 토큰 저장 + axios 헤더 설정
    await auth.fetchUser()       // ✅ 사용자 정보 가져오기

    alert(`${auth.user?.username}님, 로그인 되었습니다.`)
    router.push('/')
  } catch (err) {
    console.error('❌ 카카오 로그인 실패:', err.response?.data || err.message)
    alert('카카오 로그인 실패')
    router.push('/login')
  }
})
</script>
