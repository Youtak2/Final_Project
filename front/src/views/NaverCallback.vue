<template>
  <div>
    <p>네이버 로그인 처리 중...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

onMounted(async () => {
  const code = route.query.code
  const state = route.query.state

  if (!code || !state) {
    alert('인가 코드 또는 상태값이 없습니다.')
    router.push('/login')
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/naver/login/', {
      code,
      state,
      redirect_uri: 'http://localhost:5173/oauth/naver'  // ✅ 콘솔에 등록된 redirect URI와 일치
    })

    const token = res.data.token
    auth.setToken(token)
    await auth.fetchUser()

    alert(`${auth.user?.username}님, 네이버 로그인 되었습니다.`)
    router.push('/')
  } catch (err) {
    console.error('❌ 네이버 로그인 실패:', err.response?.data || err.message)
    alert('네이버 로그인 실패')
    router.push('/login')
  }
})
</script>
