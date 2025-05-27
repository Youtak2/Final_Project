<template>
  <div class="mypage-container">
    <h2>
      반갑습니다. {{ username }}님
      <span class="vip-inline">{{ vipLevel }}</span>
    </h2>

    <!-- 탭 -->
    <div class="tab-menu">
      <RouterLink to="/mypage">기본 정보 수정</RouterLink>
      <RouterLink to="/mypage/portfolio">포트폴리오 수정</RouterLink>
      <RouterLink to="/mypage/recommend">추천하는 상품목록</RouterLink>
      <RouterLink to="/mypage/bookmarks">찜한 상품 보기</RouterLink>
      <RouterLink to="/mypage/favorites">관심 종목 보기</RouterLink>
    </div>

    <!-- 기본 정보 카드 -->
    <div class="profile-card">
      <h3>기본 정보 수정</h3>
      <div v-for="(item, key) in userInfo" :key="key" class="info-row">
        <label>{{ key }}</label>
        <input
          :value="userInfo[key]"
          :disabled="!editable[key] || key === 'ID'"
          @input="updateValue($event, key)"
        />
        <button
          v-if="key !== 'ID'"
          class="edit-btn"
          @click="toggleEdit(key)"
        >
          {{ editable[key] ? '저장' : '수정하기' }}
        </button>
        <!-- 보유자산 VIP 뱃지 -->
        <span v-if="key === '투자금액'" class="vip-badge">{{ vipLevel }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'

const userId = ref(null)
const username = ref('')
const userInfo = reactive({})
const editable = reactive({})

// VIP 등급 계산: 투자금액(investment_amount) 기준
const vipLevel = computed(() => {
  const raw = userInfo['투자금액']?.toString().replace(/[^0-9]/g, '')
  const investAmt = Number(raw)
  if (isNaN(investAmt)) return ''
  if (investAmt >= 10000000000) return '🔥 VVVVIP'  // 100억 이상
  if (investAmt >= 1000000000) return '👑 VVIP'    // 10억 이상
  if (investAmt >= 100000000) return '💎 VIP'      // 1억 이상
  return ''
})

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/auth/user/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    const user = res.data
    userId.value = user.pk || user.id
    username.value = user.username

    Object.assign(userInfo, {
      ID: user.username,
      Email: user.email || '',
      보유자산: user.asset ?? 0,
      연봉: user.salary ?? '',
      나이: user.age ?? '',
      투자금액: user.investment_amount ?? 0   // 투자금액 필드 추가, 백엔드에서 내려줘야 함
    })

    Object.keys(userInfo).forEach(key => {
      editable[key] = false
    })
  } catch (err) {
    console.error('유저 정보 불러오기 실패:', err)
  }
})

function toggleEdit(key) {
  if (!editable[key] && ['연봉', '나이'].includes(key) && userInfo[key] === '입력해주세요') {
    userInfo[key] = ''
  }

  if (editable[key]) {
    saveField(key)
  }

  editable[key] = !editable[key]
}

function updateValue(event, key) {
  userInfo[key] = event.target.value
}

async function saveField(key) {
  const token = localStorage.getItem('token')
  if (!token) return

  const payloadMap = {
    'Email': 'email',
    '보유자산': 'asset',
    '연봉': 'salary',
    '나이': 'age',
    '투자금액': 'investment_amount'  // 서버에 맞게 필드명 조정 필요
  }

  const field = payloadMap[key]
  if (!field) return

  if (!userInfo[key]?.toString().trim()) {
    alert(`${key}은(는) 비워둘 수 없습니다.`)
    return
  }

  try {
    await axios.patch('http://127.0.0.1:8000/api/v1/accounts/update/', {
      [field]: userInfo[key]
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log(`${key} 저장 완료`)
  } catch (err) {
    console.error(`${key} 저장 실패`, err.response?.data || err)
  }
}
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
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

.vip-badge,
.vip-inline {
  margin-left: 10px;
  font-weight: bold;
  color: #e67e22;
}
</style>
