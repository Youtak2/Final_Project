<template>
  <div>
    <h2>📈 과거 시세 차트</h2>

    <!-- 티커 입력 + 조회 -->
    <div style="margin-bottom: 1rem;">
      <input v-model="keyword" placeholder="종목명 입력 (ex: apple, AAPL)" />
      <select v-model="selectedRange">
        <option v-for="opt in options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <button @click="fetchOhlcv">조회</button>
      <button @click="downloadCSV">CSV로 저장</button>
      <button @click="resetZoom">줌 초기화</button>
    </div>

    <!-- 찜하기 -->
    <div v-if="chartData" style="margin-bottom: 10px;">
      <button
        @click="toggleFavorite"
        :style="{ backgroundColor: isFavorite ? '#ff6b81' : '#f1f2f6' }"
      >
        {{ isFavorite ? '💖 찜 해제' : '🤍 찜하기' }}
      </button>
    </div>


    <!-- 차트 -->
    <div style="width: 100%; max-width: 1200px; height: 600px;">
      <Line
        v-if="chartData"
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

// ✅ 종목 맵핑 JSON import (한 번만!)
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
const keyword = ref('apple')
const lastFetchedData = ref([])
const isFavorite = ref(false)
const selectedSymbol = ref('')


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

// ✅ 종목명 또는 심볼 기반 티커 찾기
const fetchTickerByName = async (input) => {
  const lowered = input.toLowerCase()
  const found = tickerData.find(entry =>
    (entry.name && entry.name.toLowerCase() === lowered) ||
    (entry.symbol && entry.symbol.toLowerCase() === lowered)
  )
  return found ? found.symbol : null
}

// 📊 시세 조회
const fetchOhlcv = async () => {
  const ticker = await fetchTickerByName(keyword.value)
  if (!ticker) {
    alert('❌ 해당 종목명을 찾을 수 없습니다.')
    return
  }
  selectedSymbol.value = ticker
  try {
    const res = await axios.get('http://localhost:8000/api/v1/stock/', {
      params: {
        ticker,
        range: selectedRange.value
      }
    })

    lastFetchedData.value = res.data
    const labels = res.data.map(d => d.date)
    const prices = res.data.map(d => d.close)

    chartData.value = {
      labels,
      datasets: [
        {
          label: `${ticker} 종가`,
          data: prices,
          borderColor: 'blue',
          backgroundColor: 'rgba(135, 206, 250, 0.3)',
          fill: true,
          tension: 0.3
        }
      ]
    }
    await checkFavoriteStatus(ticker)

  } catch (err) {
    console.error('📉 OHLCV 조회 실패:', err)
  }
}

// 📁 CSV 저장
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
  link.setAttribute('download', `${keyword.value}_${selectedRange.value}.csv`)
  link.click()
}

// 🔄 줌 초기화
const resetZoom = () => {
  const chart = chartRef.value?.chart
  if (chart?.resetZoom) {
    chart.resetZoom()
  }
}

// 관심 종목 추가
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
      console.error('관심 종목 조회 실패:', err)
    }
  }

const toggleFavorite = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert("로그인이 필요합니다.")
    return
  }

  const headers = { Authorization: `Token ${token}` }

  try {
    if (isFavorite.value) {
      await axios.delete('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
        headers,
        data: { symbol: keyword.value.toUpperCase() }
      })
      isFavorite.value = false
    } else {
      await axios.post('/api/v1/accounts/favorites/', { symbol: selectedSymbol.value }, { headers })
      isFavorite.value = true
    }
  } catch (err) {
    console.error('찜 처리 실패:', err)
  }
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
</style>
