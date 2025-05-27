<template>
  <div>
    <!-- 카테고리 선택 버튼 -->
    <div class="category-buttons" data-aos="fade-up">
      <button :class="{ active: category === 'saving' }" @click="category = 'saving'">예금/적금</button>
      <button :class="{ active: category === 'stock' }" @click="category = 'stock'">해외주식</button>
    </div>

    <!-- 해외주식 탭 -->
    <div v-if="category === 'stock'" data-aos="fade-up" data-aos-delay="100">
      <div class="stock-wrapper">
        <h2 class="section-title">
          📊 머신러닝 기반 추천 종목 Top 20
        </h2>

        <!-- 평균 예측률: 조회 완료 후에만 표시 -->
        <p v-if="!isLoading && fetchedOnce" class="prediction">
          전체 평균 예측률: {{ isVip ? formatPercent(avgPredictionRate) : '---' }}
        </p>

        <div class="center-area" v-if="!fetchedOnce">
          <button @click="fetchRecommendations" :disabled="isLoading">
            {{ isLoading ? '🔄 분석 중...' : '🔍 해외주식 종목 추천 받기' }}
          </button>
        </div>

        <p v-if="isLoading" class="loading-message">
          <img src="/video/Loading.gif" alt="로딩 중..." class="loading-gif" />
          <br />🧠 종목 데이터를 분석 중입니다... 잠시만 기다려주세요.
        </p>
      </div>

      <p class="note">
        * 투자는 본인의 선택입니다. 종목추천은 참고 자료로 사용해주세요.<br />
        * 예측률은 VIP 등급(투자 금액 1억 이상)부터 볼 수 있습니다.
      </p>

      <table v-if="stocks.length && !isLoading">
        <thead>
          <tr>
            <th style="width: 100px;"> </th>
            <th style="width: 80px;">티커</th>
            <th style="width: 80px;">PER</th>
            <th style="width: 80px;">ROE</th>
            <th style="width: 80px;">RSI</th>
            <th style="width: 80px;">예측률</th>
            <th>추천 이유</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in stocks" :key="stock.symbol">
            <td style="width: 100px;"><FavoriteButton :symbol="stock.symbol" /></td>
            <td>{{ stock.symbol }}</td>
            <td>{{ formatNumber(stock.PER) }}</td>
            <td>{{ formatPercent(stock.ROE) }}</td>
            <td>{{ formatNumber(stock.RSI) }}</td>
            <td>{{ isVip ? formatPercent(stock.probability) : '---' }}</td>
            <td class="reason-cell">{{ stock.reason }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="!stocks.length && fetchedOnce && !isLoading">
        ⚠️ 추천된 종목이 없습니다.
      </p>
    </div>

    <!-- 예금/적금 탭 -->
    <div v-if="category === 'saving'" class="saving-wrapper" data-aos="fade-up" data-aos-delay="100">
      <h2 class="section-title">
        <span>💰 예금/적금 추천 Top 6</span>
      </h2>

      <div class="center-area" v-if="!fetchedOnceSaving">
        <button @click="fetchSavingRecommendations" :disabled="isSavingLoading">
          {{ isSavingLoading ? '🔄 분석 중...' : '🔍 예금/적금 추천 받기' }}
        </button>
      </div>

      <p v-if="isSavingLoading" class="loading-message">
        <img src="/video/Loading.gif" alt="로딩 중..." class="loading-gif" />
        <br />🧠 추천 상품을 조회 중입니다...
      </p>

      <table v-if="savingRecommendations.length && !isSavingLoading">
        <thead>
          <tr>
            <th style="width: 150px;">금융회사</th>
            <th style="width: 400px;">상품명</th>
            <th style="width: 120px;">추천 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in savingRecommendations" :key="item.상품명">
            <td>{{ item.금융회사 }}</td>
            <td>
              <RouterLink :to="`/deposit/${item.id}`" class="link">
                {{ item.상품명 }}
              </RouterLink>
            </td>
            <td>{{ formatNumber(item.추천_금리) }}%</td>
          </tr>
        </tbody>
      </table>

      <p v-if="!savingRecommendations.length && fetchedOnceSaving && !isSavingLoading">
        ⚠️ 추천된 상품이 없습니다.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import FavoriteButton from '../components/FavoriteButton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const category = ref('saving')  // 기본값 예금/적금

// 해외주식 관련
const stocks = ref([])
const fetchedOnce = ref(false)
const isLoading = ref(false)
const avgPredictionRate = ref(0)
const isVip = ref(false)

// 예금/적금 관련
const savingRecommendations = ref([])
const fetchedOnceSaving = ref(false)
const isSavingLoading = ref(false)

const token = localStorage.getItem('token')

// 해외주식 추천 호출
const fetchRecommendations = async () => {
  isLoading.value = true
  stocks.value = []
  fetchedOnce.value = false
  avgPredictionRate.value = 0
  isVip.value = false

  if (!token) {
    alert('로그인이 필요합니다')
    isLoading.value = false
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/recommend/', {
      headers: { Authorization: `Token ${token}` }
    })
    stocks.value = res.data.stock_recommendations
    avgPredictionRate.value = res.data.average_prediction_rate || 0
    isVip.value = res.data.is_vip || false
  } catch (err) {
    console.error('API 요청 실패:', err)
    if (err.response?.status === 400 && err.response.data?.redirect) {
      alert(err.response.data.error || '설정이 필요합니다.')
      router.push(err.response.data.redirect)
    }
  } finally {
    isLoading.value = false
    fetchedOnce.value = true
  }
}

// 예금/적금 추천 호출
const fetchSavingRecommendations = async () => {
  isSavingLoading.value = true
  savingRecommendations.value = []
  fetchedOnceSaving.value = false

  if (!token) {
    alert('로그인이 필요합니다')
    isSavingLoading.value = false
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/recommend/savings/', {
      headers: { Authorization: `Token ${token}` }
    })
    savingRecommendations.value = res.data.map(item => ({
      id: item.id,
      금융회사: item['금융회사'],
      상품명: item['상품명'],
      추천_금리: item['추천_금리']
    }))
  } catch (err) {
    console.error('예금/적금 API 요청 실패:', err)
  } finally {
    isSavingLoading.value = false
    fetchedOnceSaving.value = true
  }
}

const formatNumber = (val) => {
  if (val === null || val === undefined) return '-'
  return Number(val).toLocaleString(undefined, { maximumFractionDigits: 2 })
}

const formatPercent = (val) => {
  if (val === null || val === undefined) return '-'
  return `${(val * 100).toFixed(1)}%`
}
</script>

<style scoped>
div {
  font-family: 'Pretendard', sans-serif;
  color: #1E3A8A;
  max-width: 1000px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #f9fafb;
}

.section-title {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
}

.prediction {
  font-weight: bold;
  font-size: 1rem;
}

.category-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.category-buttons button {
  padding: 0.6rem 1.4rem;
  border-radius: 9999px;
  border: 2px solid #1E3A8A;
  background-color: white;
  color: #1E3A8A;
  font-weight: 600;
  transition: 0.3s;
}

.category-buttons button.active,
.category-buttons button:hover {
  background-color: #3B82F6;
  border-color: #3B82F6;
  color: white;
}

button {
  background-color: #3B82F6;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: 0.3s;
}

button:hover {
  background-color: #1E3A8A;
}

button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  margin-top: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
}

th,
td {
  padding: 0.75rem;
  text-align: center;
  font-size: 0.95rem;
  border-bottom: 1px solid #f1f5f9;
}

.reason-cell {
  text-align: left;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
  line-height: 1.4;
}

p.note {
  margin-top: 1rem;
  color: #6B7280;
  font-size: 0.9rem;
  line-height: 1.5;
}

.link {
  color: #1E3A8A;
  font-weight: 600;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.saving-wrapper {
  text-align: center;
}
.center-area {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.prediction {
  font-weight: bold;
  font-size: 1rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

</style>

