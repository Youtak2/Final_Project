<template>
  <div class="chart-page" data-aos="fade-up">
    <h2 data-aos="fade-up" data-aos-delay="100">📈 과거 시세 차트</h2>

    <div class="toolbar" style="margin-bottom: 1rem; position: relative;" data-aos="fade-up" data-aos-delay="200">
      <input
        v-model="searchTerm"
        placeholder="종목명 입력 (ex: apple, AAPL)"
        @input="onInput"
        @keydown.down.prevent="moveDown"
        @keydown.up.prevent="moveUp"
        @keydown.enter.prevent="selectHighlighted"
        autocomplete="off"
      />
      <ul v-if="suggestions.length" class="autocomplete-list">
        <li
          v-for="(item, index) in suggestions"
          :key="item.symbol"
          :class="{ highlighted: index === highlightedIndex }"
          @mousedown.prevent="selectSuggestion(item)"
        >
          {{ item.name }} ({{ item.symbol }})
        </li>
      </ul>

      <select v-model="selectedRange">
        <option v-for="opt in options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <button @click="fetchOhlcv">조회</button>
      <button @click="downloadCSV">CSV로 저장</button>
      <button @click="resetZoom">줌 초기화</button>
    </div>

    <!-- 찜 버튼 -->
    <div class="favorite-toggle" v-if="chartData && lastFetchedData.length > 0" style="margin-bottom: 10px;">
      <button
        @click="toggleFavorite"
        :style="{ backgroundColor: isFavorite ? '#ff6b81' : '#f1f2f6' }"
      >
        {{ isFavorite ? '💖 찜 해제' : '🤍 찜하기' }}
      </button>
    </div>

    <!-- 차트 또는 로딩 -->
    <div class="chart-wrapper" style="width: 100%; max-width: 1200px; height: 600px;">
      <div v-if="isLoading" class="loading-message">
        <img src="/video/Loading.gif" alt="로딩 중..." class="loading-gif" />
        <p style="text-align: center; color: #3B82F6;">🔄 데이터를 불러오는 중입니다...</p>
      </div>

      <Line
        v-else-if="chartData"
        :data="chartData"
        :options="chartOptions"
        ref="chartRef"
      />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Filler
} from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { Line } from 'vue-chartjs'
import tickerData from '@/assets/tickers.json'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Filler,
  zoomPlugin
)

const chartRef = ref(null)
const chartData = ref(null)
const selectedRange = ref('1w')
const searchTerm = ref('')
const suggestions = ref([])
const highlightedIndex = ref(-1)
const lastFetchedData = ref([])
const isFavorite = ref(false)
const selectedSymbol = ref('')
const isLoading = ref(false)


const options = [
  { label: '1일', value: '1d' },
  { label: '1주일', value: '1w' },
  { label: '1개월', value: '1m' },
  { label: '3개월', value: '3m' },
  { label: '1년', value: '1y' }
]

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    zoom: {
      pan: { enabled: true, mode: 'x' },
      zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'x' }
    },
    legend: { position: 'top' }
  },
  interaction: {
    mode: 'index',
    intersect: false
  },
  scales: {
    x: {
      ticks: {
        autoSkip: true,
        maxRotation: 0
      }
    }
  }
}

const fetchTickerByName = async (input) => {
  const lowered = input.toLowerCase()
  const found = tickerData.find(entry =>
    (entry.name && entry.name.toLowerCase() === lowered) ||
    (entry.symbol && entry.symbol.toLowerCase() === lowered)
  )
  return found ? found.symbol : null
}

const fetchOhlcv = async () => {
  if (!selectedSymbol.value) {
    const ticker = await fetchTickerByName(searchTerm.value)
    if (!ticker) {
      alert('❌ 해당 종목명을 찾을 수 없습니다.')
      return
    }
    selectedSymbol.value = ticker
  }

  isLoading.value = true  // ✅ 시작

  try {
    const token = localStorage.getItem('token')
    const headers = token ? { Authorization: `Token ${token}` } : {}

    const res = await axios.get('http://localhost:8000/api/v1/stock/', {
      params: {
        ticker: selectedSymbol.value,
        range: selectedRange.value
      },
      headers
    })

    if (!res.data || !Array.isArray(res.data.prices)) {
      alert('가격 데이터가 없습니다.')
      return
    }

    lastFetchedData.value = res.data.prices
    const labels = res.data.prices.map(d => d.date)
    const prices = res.data.prices.map(d => d.close)

    chartData.value = {
      labels,
      datasets: [
        {
          label: `${selectedSymbol.value} 종가`,
          data: prices,
          borderColor: 'blue',
          backgroundColor: 'rgba(135, 206, 250, 0.3)',
          fill: true,
          tension: 0.3
        }
      ]
    }

    await checkFavoriteStatus(selectedSymbol.value)
  } catch (err) {
    console.error('📉 OHLCV 조회 실패:', err)
  } finally {
    isLoading.value = false // ✅ 종료
  }
}

const checkFavoriteStatus = async (ticker) => {
  const token = localStorage.getItem('token')
  if (!token) {
    isFavorite.value = false
    return
  }
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
      headers: { Authorization: `Token ${token}` }
    })
    isFavorite.value = res.data.some(item => item.symbol === ticker)
  } catch (err) {
    console.error('찜 여부 확인 실패:', err)
  }
}

const toggleFavorite = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요합니다.')
    return
  }
  const headers = { Authorization: `Token ${token}` }
  try {
    if (isFavorite.value) {
      await axios.delete('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
        headers,
        data: { symbol: selectedSymbol.value }
      })
      isFavorite.value = false
    } else {
      await axios.post('http://127.0.0.1:8000/api/v1/accounts/favorites/', 
        { symbol: selectedSymbol.value },
        { headers })
      isFavorite.value = true
    }
  } catch (err) {
    console.error('찜 처리 실패:', err)
  }
}

const downloadCSV = () => {
  if (!lastFetchedData.value.length) {
    alert('먼저 데이터를 조회하세요.')
    return
  }
  const header = Object.keys(lastFetchedData.value[0]).join(',')
  const rows = lastFetchedData.value.map(row => Object.values(row).join(','))
  const csvContent = [header, ...rows].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', `${searchTerm.value}_${selectedRange.value}.csv`)
  link.click()
}

const resetZoom = () => {
  const chart = chartRef.value?.chart
  if (chart?.resetZoom) {
    chart.resetZoom()
  }
}

const onInput = async () => {
  const val = searchTerm.value.trim()
  if (val.length < 2) {
    suggestions.value = []
    return
  }

  const lowered = val.toLowerCase()
  suggestions.value = tickerData.filter(item =>
    (item.name && item.name.toLowerCase().includes(lowered)) ||
    (item.symbol && item.symbol.toLowerCase().includes(lowered))
  ).slice(0, 10)

  highlightedIndex.value = -1
}

const moveDown = () => {
  if (highlightedIndex.value < suggestions.value.length - 1) {
    highlightedIndex.value++
  }
}

const moveUp = () => {
  if (highlightedIndex.value > 0) {
    highlightedIndex.value--
  }
}

const selectHighlighted = () => {
  if (highlightedIndex.value >= 0 && highlightedIndex.value < suggestions.value.length) {
    selectSuggestion(suggestions.value[highlightedIndex.value])
  }
}

const selectSuggestion = (item) => {
  searchTerm.value = item.name
  selectedSymbol.value = item.symbol
  suggestions.value = []
  fetchOhlcv()
}
</script>

<style scoped>
input {
  padding: 4px;
  margin-right: 8px;
}
select {
  margin-right: 8px;
}
button {
  margin-right: 6px;
  padding: 5px 10px;
  cursor: pointer;
}
button.active {
  background-color: #1976d2;
  color: white;
}
.autocomplete-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 240px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ccc;
  border-top: none;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10;
}
.autocomplete-list li {
  padding: 8px 12px;
  cursor: pointer;
}
.autocomplete-list li.highlighted,
.autocomplete-list li:hover {
  background-color: #e6f0ff;
}

.chart-page {
  max-width: 960px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.chart-page h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1E3A8A;
  margin-bottom: 1.5rem;
  text-align: center;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
}

.toolbar input,
.toolbar select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.toolbar button {
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.toolbar button:hover {
  background-color: #2563eb;
}

.favorite-toggle {
  text-align: center;
  margin-bottom: 1.5rem;
}

.favorite-toggle button {
  background-color: #f1f2f6;
  color: #111;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  cursor: pointer;
  font-weight: 600;
}

.favorite-toggle button.active {
  background-color: #EF4444;
  color: white;
}

.chart-wrapper {
  width: 100%;
  height: 600px;
  padding: 1rem;
}

.loading-gif {
  width: 200px;
  height: auto;
  display: block;
  margin: 0 auto;
}

</style>
