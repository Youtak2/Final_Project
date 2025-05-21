<template>
  <div>로그인 처리 중...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const code = route.query.code
  if (code) {
    try {
      const res = await axios.post('http://localhost:8000/api/v1/auth/kakao/', { code })
      localStorage.setItem('token', res.data.token)
      alert(`${res.data.nickname}님, 로그인 되었습니다.`)
      router.push('/')
    } catch (err) {
      alert('로그인 실패')
    }
  }
})
</script>