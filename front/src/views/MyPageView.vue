<template>
  <div class="mypage-container">
    <h2>{{ username }} 님의 프로필 페이지</h2>

    <!-- 탭 -->
    <div class="tab-menu">
      <RouterLink to="/mypage">기본 정보 수정</RouterLink>
      <RouterLink to="/mypage/portfolio">포트폴리오 수정</RouterLink>
      <RouterLink to="/mypage/recommend">상품 추천 받기</RouterLink>
    </div>

    <!-- 기본 정보 카드 -->
    <div class="profile-card">
      <h3>기본 정보 수정</h3>
      <div v-for="(item, key) in userInfo" :key="key" class="info-row">
        <label>{{ key }}</label>
        <input :value="item" disabled />
        <button class="edit-btn">수정하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const username = ref('')
const userInfo = ref({})

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/auth/user/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 응답으로 받은 사용자 정보 설정
    const user = res.data
    username.value = user.username
    userInfo.value = {
      ID: user.username,
      Email: user.email,
      Nickname: user.first_name || '닉네임을 설정해주세요',
      나이: '입력해주세요',           // 추가 정보는 백엔드에서 제공하도록 확장 가능
      현재가입금액: '0',
      연봉: '입력해주세요'
    }
  } catch (err) {
    console.error('유저 정보 불러오기 실패:', err)
  }
})
</script>


<style scoped>
.mypage-container {
  max-width: 700px;
  margin: 2rem auto;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  font-family: sans-serif;
}

h2 {
  background-color: #00b894;
  color: white;
  padding: 1rem;
  text-align: center;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.tab-menu {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.tab-menu a {
  text-decoration: none;
  font-weight: bold;
  color: #333;
  padding: 0.5rem;
}

.profile-card {
  border-top: 1px solid #ccc;
  padding-top: 1rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1rem;
}

.info-row label {
  width: 120px;
  text-align: right;
  font-weight: bold;
}

.info-row input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.edit-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>
