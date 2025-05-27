<template>
  <div>
    <input v-model="symbolInput" placeholder="종목명 입력 (ex: apple, AAPL)" />
    <ul v-if="symbolInput && filteredTickers.length">
      <li
        v-for="item in filteredTickers"
        :key="item.symbol"
        @click="selectTicker(item)"
      >
        {{ item.name }} ({{ item.symbol }})
      </li>
    </ul>

    <button @click="search">조회</button>

    <div v-if="symbol">
      <div style="margin: 10px 0;">
        <button @click="load('income')">손익계산서</button>
        <button @click="load('balance')">대차대조표</button>
        <button @click="load('cashflow')">현금흐름표</button>
      </div>

      <div style="margin-bottom: 10px;">
        <button @click="changePeriod('annual')" :disabled="selectedPeriod === 'annual'">📅 연간</button>
        <button @click="changePeriod('quarterly')" :disabled="selectedPeriod === 'quarterly'">📆 분기</button>
      </div>

      <div class="stock-card">
        <h3>{{ symbol }}</h3>
        <button @click="toggleFavorite">{{ isFavorite ? '💖 찜 해제' : '🤍 찜하기' }}</button>
      </div>

      <!-- ✅ 차트 -->
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />

      <!-- ✅ 표 -->
      <table v-if="columns.length && rows.length">
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import KOREAN_LABELS from "@/assets/korean_labels.json"
import tickers from "@/assets/tickers.json"
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

const changePeriod = (p) => {
  selectedPeriod.value = p
  load(currentType.value)
}

const currentType = ref('income')

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

const formatNumber = (val) => {
  if (!val && val !== 0) return ''
  return Number(val).toLocaleString()
}

// ✅ 차트 구성
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

// 관심 종목 등록
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

import { watch } from 'vue'

// 종목 변경될 때마다 찜 상태 갱신
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
  const token = localStorage.getItem('token')
  if (!token) {
    alert("로그인이 필요합니다.")
    return
  }

  const headers = { Authorization: `Token ${token}` }

  try {
    // 찜 상태 변경 (찜 해제 / 찜 하기)
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
}  // ✅ 여기가 누락되었음

</script>

<style scoped>
input {
  padding: 6px;
  margin-bottom: 10px;
  width: 300px;
}
ul {
  list-style: none;
  padding: 0;
  margin-top: 4px;
  max-height: 150px;
  overflow-y: auto;
  border: 1px solid #ccc;
}
li {
  padding: 4px;
  cursor: pointer;
}
li:hover {
  background-color: #f0f0f0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  padding: 6px;
  border: 1px solid #ddd;
  text-align: right;
}
th:first-child, td:first-child {
  text-align: left;
}
</style>
