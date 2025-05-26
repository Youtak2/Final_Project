<template>
  <div>구글 로그인 처리 중...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

onMounted(async () => {
  const hash = window.location.hash.substr(1)
  const params = new URLSearchParams(hash)
  const accessToken = params.get('access_token')

  if (!accessToken) {
    alert('구글 로그인 토큰을 받지 못했습니다.')
    router.push('/login')
    return
  }

  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/google/login/', {
      access_token: accessToken
    })

    auth.setToken(res.data.key)

    router.push('/')
  } catch (error) {
    alert('로그인 실패')
    router.push('/login')
  }
})
</script>
