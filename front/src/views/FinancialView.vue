<template>
  <div class="financial-wrapper">
    <div class="center-container">
      <h2 class="section-title" data-aos="fade-up">📊 종목 한 입 진단</h2>
      <!-- 검색 영역 -->
      <div class="search-section" data-aos="fade-up" data-aos-delay="100">
        <div class="autocomplete-area">
          <div class="autocomplete-wrapper">
            <input v-model="symbolInput" placeholder="종목명 입력 (ex: apple, AAPL)" ref="symbolInputRef" @keyup.enter="search"/>
            <button @click="search">조회</button>
          </div>
          <ul v-if="symbolInput && filteredTickers.length" class="autocomplete-list">
            <li
              v-for="item in filteredTickers"
              :key="item.symbol"
              @click="selectTicker(item)"
            >
              {{ item.name }} ({{ item.symbol }})
            </li>
          </ul>
        </div>
      </div>

      <!-- 결과 영역 -->
      <div v-if="symbol" class="result-area">
        <div class="button-group">
          <button :class="{ active: currentType === 'income' }" @click="load('income')">손익계산서</button>
          <button :class="{ active: currentType === 'balance' }" @click="load('balance')">대차대조표</button>
          <button :class="{ active: currentType === 'cashflow' }" @click="load('cashflow')">현금흐름표</button>
        </div>

        <div class="button-group">
          <button :class="{ active: selectedPeriod === 'annual' }" @click="changePeriod('annual')">📅 연간</button>
          <button :class="{ active: selectedPeriod === 'quarterly' }" @click="changePeriod('quarterly')">📆 분기</button>
        </div>

        <div class="stock-card">
          <h3>{{ symbol }}</h3>
          <button @click="toggleFavorite">{{ isFavorite ? '💖 찜 해제' : '🤍 찜하기' }}</button>
        </div>

        <transition name="fade-slide" mode="out-in">
          <Bar
            v-if="chartData"
            :data="chartData"
            :options="chartOptions"
            key="financial-bar"
          />
        </transition>

        <transition name="fade-slide" mode="out-in">
          <table v-if="columns.length && rows.length" key="financial-table">
            <thead>
              <tr>
                <th>항목</th>
                <th v-for="col in columns" :key="col">{{ col }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in rows" :key="row">
                <td>{{ KOREAN_LABELS[row] || row }}</td>
                <td v-for="col in columns" :key="col">{{ formatNumber(financials[col][row]) }}</td>
              </tr>
            </tbody>
          </table>
        </transition>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import KOREAN_LABELS from '../assets/korean_labels.json'
import tickers from '../assets/tickers.json'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const symbolInput = ref('')
const symbol = ref('')
const selectedPeriod = ref('quarterly')
const financials = ref({})
const columns = ref([])
const rows = ref([])
const isFavorite = ref(false)
const token = localStorage.getItem('token')
const symbolInputRef = ref(null)

const filteredTickers = computed(() => {
  const keyword = symbolInput.value.toLowerCase()
  return tickers.filter(
    t => t.symbol.toLowerCase().includes(keyword) || t.name.toLowerCase().includes(keyword)
  ).slice(0, 10)
})

const selectTicker = (item) => {
  symbolInput.value = `${item.name} (${item.symbol})`
  symbol.value = item.symbol
}

const currentType = ref('income')
const changePeriod = (p) => {
  selectedPeriod.value = p
  load(currentType.value)
}

const load = async (type) => {
  currentType.value = type
  if (!symbol.value) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/financial/financials/', {
      params: {
        symbol: symbol.value,
        type: type,
        period: selectedPeriod.value,
      }
    })
    financials.value = res.data
    columns.value = Object.keys(financials.value)
    rows.value = Object.keys(financials.value[columns.value[0]] || {})
  } catch (err) {
    console.error(err)
  }
}

const search = () => {
  const match = symbolInput.value.match(/\((.*?)\)$/)
  symbol.value = match ? match[1] : symbolInput.value
  load(currentType.value)
}

// 예: 억/조 단위로 표시하거나 %, 배수로 변환
const formatNumber = (val) => {
  if (val === null || val === undefined || val === '') return '-'
  const num = Number(val)
  if (isNaN(num)) return val
  if (Math.abs(num) >= 1e12) return `\$${(num / 1e12).toFixed(2)}T`
  if (Math.abs(num) >= 1e9)  return `\$${(num / 1e9).toFixed(2)}B`
  if (Math.abs(num) >= 1e6)  return `\$${(num / 1e6).toFixed(2)}M`
  return `\$${num.toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })}`
}



const chartData = computed(() => {
  if (!columns.value.length || !rows.value.includes('Net Income')) return null
  return {
    labels: columns.value,
    datasets: [{
      label: 'Net Income',
      backgroundColor: '#42a5f5',
      data: columns.value.map(col => financials.value[col]['Net Income'] || 0)
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    }
  }
}

onMounted(async () => {
  if (!token || !symbol.value) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
      headers: { Authorization: `Token ${token}` }
    })
    isFavorite.value = res.data.some(item => item.symbol === symbol.value)
  } catch (err) {
    console.error('관심 종목 조회 실패:', err)
  }
})

watch(symbol, async (newSymbol) => {
  if (!token || !newSymbol) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
      headers: { Authorization: `Token ${token}` }
    })
    isFavorite.value = res.data.some(item => item.symbol === newSymbol)
  } catch (err) {
    console.error('찜 상태 확인 실패:', err)
  }
})

const toggleFavorite = async () => {
  if (!token) {
    alert("로그인이 필요합니다.")
    return
  }

  const headers = { Authorization: `Token ${token}` }

  try {
    if (isFavorite.value) {
      await axios.delete('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
        headers,
        data: { symbol: symbol.value }
      })
      isFavorite.value = false
    } else {
      await axios.post('http://127.0.0.1:8000/api/v1/accounts/favorites/',
        { symbol: symbol.value },
        { headers }
      )
      isFavorite.value = true
    }
  } catch (err) {
    console.error('찜 처리 실패:', err)
  }
}

onMounted(() => {
  symbolInputRef.value?.focus()
})

</script>

<style scoped>
:root {
  --blue-dark: #1E3A8A;
  --blue-main: #3B82F6;
  --red-main: #EF4444;
  --bg-light: #F9FAFB;
  --line-gray: #E5E7EB;
}

.financial-wrapper {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  width: 100%;
}

.center-container {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-section {
  width: 100%;
  margin-bottom: 2rem;
}

.autocomplete-area {
  position: relative;
  width: 100%;
}

.autocomplete-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  gap: 10px;
}

input {
  width: 300px; /* 고정 너비 */
  padding: 10px 12px;
  border: 1px solid var(--line-gray);
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

button {
  padding: 8px 16px;
  font-size: 0.9rem;
  border-radius: 8px;
  border: none;
  background-color: var(--blue-main);
  color: white;
  cursor: pointer;
  transition: 0.2s;
  flex-shrink: 0;
}

button:hover {
  opacity: 0.9;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.autocomplete-list {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  z-index: 10;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin: 4px 0 0;
  padding: 0;
}
.autocomplete-list li {
  padding: 8px 12px;
  cursor: pointer;
}
.autocomplete-list li:hover {
  background-color: #f0f4ff;
}

.result-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.button-group button {
  min-width: 110px;
  padding: 10px 16px;
  font-size: 0.95rem;
  border-radius: 8px;
  text-align: center;
  background-color: #dbeafe; /* 비선택 상태 연한 파랑 */
  color: #1e3a8a;
  border: none;
  transition: 0.2s ease;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px; 
}

.stock-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 800px;
  padding: 1rem;
  background: white;
  border: 1px solid var(--line-gray);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.stock-card h3 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--blue-dark);
}

.Bar {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 12px;
  padding: 1rem;
  margin: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

table {
  width: 100%;
  max-width: 800px;
  background: white;
  border-collapse: collapse;
  border-radius: 8px;
  margin-top: 20px;
  border: 1px solid var(--line-gray);
  overflow: hidden;
}

th, td {
  white-space: nowrap;
  padding: 10px 12px;
  border: 1px solid var(--line-gray);
  text-align: right;
  font-size: 0.95rem;
}

th:first-child, td:first-child {
  text-align: left;
}

/* Hover 시 효과 */
.button-group button:hover {
  background-color: #bfdbfe;
}

/* 선택된 버튼 */
.button-group button.active {
  background-color: var(--blue-main);
  color: white;
  font-weight: 600;
}

/* 표 등장 애니메이션 */
.fade-slide-enter-active {
  transition: all 0.4s ease;
}
.fade-slide-leave-active {
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

table {
  width: 100%;
  max-width: 800px;
  background: white;
  border-collapse: collapse;
  border-radius: 8px;
  margin-top: 20px;
  border: 1px solid var(--line-gray);
  overflow: hidden;
  font-size: 0.95rem;
  text-align: center;
}

th {
  background-color: #eff6ff;
  color: #1e3a8a;
  font-weight: 700;
  padding: 12px;
  border-bottom: 1px solid #ddd;
}

td {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}

tbody tr:hover {
  background-color: #f9fafb;
}

.section-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: var(--blue-dark);
  margin-bottom: 1.5rem;
  text-align: center;
}


</style>
