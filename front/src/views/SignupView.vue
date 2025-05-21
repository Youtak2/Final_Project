<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignup">
    <div>
        <label>성함:</label>
        <input v-model="name" type="text" required />
      </div>
      <div>
        <label>아이디:</label>
        <input v-model="username" type="text" required />
        <button type="button" @click="checkUsername">중복 체크</button>
        <p v-if="usernameStatus === 'available'" class="status available">사용 가능한 아이디입니다.</p>
        <p v-if="usernameStatus === 'taken'" class="status taken">이미 사용 중인 아이디입니다.</p>
      </div>



      <div>
        <label>비밀번호:</label>
        <input v-model="password" type="password" required />
      </div>

      <div>
        <label>비밀번호 확인:</label>
        <input v-model="password2" type="password" required />
        <p v-if="passwordMismatch" class="status taken">비밀번호가 일치하지 않습니다.</p>
      </div>

      <button type="submit">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const name = ref('') // 성함
const password = ref('')
const password2 = ref('')
const usernameStatus = ref(null)
const router = useRouter()

const passwordMismatch = computed(() => {
  return password.value && password2.value && password.value !== password2.value
})

const checkUsername = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/check-username/?username=${username.value}`)
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
      username: username.value,
      name: name.value, // 이름 추가
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
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.status.available {
  color: green;
}

.status.taken {
  color: red;
}
</style>
