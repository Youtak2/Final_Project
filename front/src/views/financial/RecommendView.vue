<template>
  <div>
    <!-- 카테고리 선택 버튼 -->
    <div class="category-buttons">
      <button :class="{ active: category === 'saving' }" @click="category = 'saving'">예금/적금</button>
      <button :class="{ active: category === 'stock' }" @click="category = 'stock'">해외주식</button>
    </div>

    <!-- 해외주식 탭 -->
    <div v-if="category === 'stock'">
      <h2 style="display: flex; justify-content: space-between; align-items: center;">
        <span>📊 머신러닝 기반 추천 종목 Top 20</span>
        <span style="font-weight: bold; font-size: 1rem;">
          전체 평균 예측률: {{ isVip ? formatPercent(avgPredictionRate) : '---' }}
        </span>
      </h2>

      <button @click="fetchRecommendations" :disabled="isLoading">
        {{ isLoading ? '🔄 분석 중...' : '🔍 해외주식 종목 추천 받기' }}
      </button>

      <p v-if="isLoading">🧠 종목 데이터를 분석 중입니다... 잠시만 기다려주세요.</p>

      <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
        * 투자는 본인의 선택입니다. 종목추천은 참고 자료로 사용해주세요.<br />
        * 예측률은 VIP 등급(투자 금액 1억 이상)부터 볼 수 있습니다.
      </p>

      <table v-if="stocks.length && !isLoading">
        <thead>
          <tr>
            <th>-</th>
            <th>티커</th>
            <th>PER</th>
            <th>ROE</th>
            <th>RSI</th>
            <th>예측률</th>
            <th>추천 이유</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stock in stocks" :key="stock.symbol">
            <td><FavoriteButton :symbol="stock.symbol" /></td>
            <td>{{ stock.symbol }}</td>
            <td>{{ formatNumber(stock.PER) }}</td>
            <td>{{ formatPercent(stock.ROE) }}</td>
            <td>{{ formatNumber(stock.RSI) }}</td>
            <td>{{ isVip ? formatPercent(stock.probability) : '---' }}</td>
            <td style="text-align: left;">{{ stock.reason }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="!stocks.length && fetchedOnce && !isLoading">
        ⚠️ 추천된 종목이 없습니다.
      </p>
    </div>

    <!-- 예금/적금 탭 -->
    <div v-if="category === 'saving'">
      <h2>예금/적금 추천 Top 6</h2>

      <button @click="fetchSavingRecommendations" :disabled="isSavingLoading">
        {{ isSavingLoading ? '🔄 분석 중...' : '🔍 예금/적금 추천 받기' }}
      </button>

      <p v-if="isSavingLoading">🧠 추천 상품을 조회 중입니다...</p>

      <table v-if="savingRecommendations.length && !isSavingLoading">
        <thead>
          <tr>
            <th>금융회사</th>
            <th>상품명</th>
            <th>추천 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in savingRecommendations" :key="item.상품명">
            <td>{{ item.금융회사 }}</td>
            <td>{{ item.상품명 }}</td>
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
import FavoriteButton from "@/components/FavoriteButton.vue"
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
      금융회사: item['금융회사'],
      상품명: item['상품명'],
      추천_금리: item['추천_금리']
    }))
  } catch (err) {
    console.error('예금/적금 API 요청 실패:', err)
    
    // ✅ 설정 누락 등의 이유로 400 내려올 때 대응
    if (err.response?.status === 400 && err.response.data?.redirect) {
      alert(err.response.data.error || '설정이 필요합니다.')
      router.push(err.response.data.redirect)
    }
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
    console.error('해외주식 추천 API 요청 실패:', err)

    // ✅ 설정 누락으로 인한 400 오류 처리
    if (err.response?.status === 400 && err.response.data?.redirect) {
      alert(err.response.data.error || '설정이 필요합니다.')
      router.push(err.response.data.redirect)
    }
  } finally {
    isLoading.value = false
    fetchedOnce.value = true
  }
}
</script>

<style scoped>
.category-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.category-buttons button {
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 6px;
  border: 1px solid #ccc;
  background: #f8f8f8;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.category-buttons button.active,
.category-buttons button:hover {
  background-color: #00b894;
  color: white;
  border-color: #00b894;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  padding: 8px;
  border: 1px solid #ccc;
  text-align: center;
}

td:last-child {
  text-align: left;
  max-width: 400px;
}

button {
  margin: 10px 0;
  padding: 6px 12px;
  cursor: pointer;
}
</style>
