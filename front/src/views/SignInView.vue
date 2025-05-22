<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label>아이디</label>
        <input v-model="username" type="text" required placeholder="아이디 입력" />
      </div>
      <div class="form-group">
        <label>비밀번호</label>
        <input v-model="password" type="password" required placeholder="비밀번호 입력" />
      </div>
      <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const login = async () => {
  try {
const res = await axios.post('http://127.0.0.1:8000/api/v1/auth/login/', {
  username: username.value,
  password: password.value
})
localStorage.setItem('token', res.data.key)  // ✅ 수정된 부분

    router.push('/').then(() => {
      window.location.reload()
    })
  } catch (err) {
    errorMessage.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
    console.error('로그인 실패:', err)
  }
}

</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.error-msg {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>
