<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignup">
      <!-- 이름 -->
      <div class="form-group">
        <label>이름</label>
        <input v-model="name" type="text" required placeholder="이름 입력" />
      </div>

      <!-- 이메일 -->
      <div class="form-group">
        <label>이메일</label>
        <input v-model="email" type="email" required placeholder="이메일 입력" />
      </div>

      <!-- 아이디 -->
      <div class="form-group">
        <label>아이디</label>
        <div class="inline-field">
          <input v-model="username" type="text" required placeholder="아이디 (6~20자)" />
          <button type="button" @click="checkUsername">중복 확인</button>
        </div>
        <p v-if="usernameStatus === 'available'" class="status available">사용 가능한 아이디입니다.</p>
        <p v-if="usernameStatus === 'taken'" class="status taken">이미 사용 중인 아이디입니다.</p>
      </div>

      <!-- 비밀번호 -->
      <div class="form-group">
        <label>비밀번호</label>
        <input v-model="password" type="password" required placeholder="8~20자: 영문, 숫자, 특수문자 조합" />
      </div>

      <!-- 비밀번호 확인 -->
      <div class="form-group">
        <label>비밀번호 확인</label>
        <input v-model="password2" type="password" required placeholder="비밀번호 확인" />
        <p v-if="passwordMismatch" class="status taken">비밀번호가 일치하지 않습니다.</p>
      </div>

      <!-- 제출 -->
      <button type="submit" class="signup-button">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const name = ref('')
const email = ref('')
const username = ref('')
const password = ref('')
const password2 = ref('')
const usernameStatus = ref(null)

const passwordMismatch = computed(() => {
  return password.value && password2.value && password.value !== password2.value
})

const checkUsername = async () => {
  try {
    const res = await axios.get(`/api/v1/accounts/check-username/?username=${username.value}`)
    usernameStatus.value = res.data.available ? 'available' : 'taken'
  } catch (err) {
    console.error('중복 체크 실패:', err)
  }
}

const handleSignup = async () => {
  if (passwordMismatch.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }
  if (usernameStatus.value !== 'available') {
    alert('아이디 중복 확인을 해주세요.')
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/v1/accounts/signup/', {
      name: name.value,
      email: email.value,
      username: username.value,
      password: password.value,
      password2: password2.value
    })
    alert('회원가입이 완료되었습니다.')
    router.push('/login')
  } catch (err) {
    console.error('회원가입 실패:', err)
    alert('회원가입에 실패했습니다.')
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 450px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
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

.inline-field {
  display: flex;
  gap: 10px;
  align-items: center;
}

.inline-field input {
  flex: 1;
}

button {
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
}

.signup-button {
  width: 100%;
  margin-top: 1rem;
  background-color: #00c471;
}

.status {
  font-size: 0.9rem;
  margin-top: 0.4rem;
}

.status.available {
  color: green;
}

.status.taken {
  color: red;
}
</style>
