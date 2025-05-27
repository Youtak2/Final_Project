<template>
  <div>
    <h2>📰 뉴스 요약 검색</h2>
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

    <button @click="search" :disabled="loading">요약 시작</button>
    <div v-if="loading">요약 중입니다...</div>

    <div v-if="results.length">
      <h3>요약 결과</h3>

      <FavoriteButton :symbol="selectedSymbol" />

      <ul>
        <li v-for="r in results" :key="r.link">
          <strong>{{ r.title }}</strong> - {{ r.impact }}<br />
          <p>{{ r.translated_summary }}</p>
          <a :href="r.link" target="_blank">원문 보기</a>
        </li>
      </ul>

      <div class="chart-box">
        <h3>📊 감성 분석 통계</h3>
        <canvas id="sentimentChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, computed } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import tickers from "@/assets/tickers.json"
import FavoriteButton from "@/components/FavoriteButton.vue"


const symbolInput = ref('')
const selectedSymbol = ref('')
const loading = ref(false)
const results = ref([])
let chartInstance = null

const filteredTickers = computed(() => {
  const keyword = symbolInput.value.toLowerCase()
  return tickers.filter(
    t => t.symbol.toLowerCase().includes(keyword) || t.name.toLowerCase().includes(keyword)
  ).slice(0, 10)
})

const selectTicker = (item) => {
  selectedSymbol.value = item.symbol
  symbolInput.value = `${item.name} (${item.symbol})`
  filteredTickers.value = []
}


const renderChart = () => {
  const counts = { 긍정: 0, 부정: 0, 중립: 0, 기타: 0 }

  for (const r of results.value) {
    const key = r.impact?.trim()
    console.log("감성 키워드:", key)

    if (key && counts.hasOwnProperty(key)) {
      counts[key]++
    } else {
      counts.기타++
    }
  } // ✅ ← for 루프 닫는 중괄호

  const ctx = document.getElementById('sentimentChart')
  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(counts),
      datasets: [
        {
          data: Object.values(counts),
          backgroundColor: ['#4caf50', '#f44336', '#9e9e9e', '#cccccc']
        }
      ]
    }
  })
}


const search = async () => {
  if (!selectedSymbol.value) return alert('종목을 선택해주세요')
  loading.value = true
  results.value = []

  try {
    await axios.get(`/api/v1/news/crawl/?symbol=${selectedSymbol.value}`)
    await axios.post(`/api/v1/news/summarize/`, { symbol: selectedSymbol.value })
    const res = await axios.get(`/api/v1/news/result/?symbol=${selectedSymbol.value}`)
    results.value = res.data.results
    await nextTick()
    renderChart()
  } catch (e) {
    console.error(e)
    alert('요약에 실패했습니다.')
  }

  loading.value = false
}

if (!selectedSymbol.value) {
  const match = symbolInput.value.match(/\((.*?)\)$/)
  selectedSymbol.value = match ? match[1] : symbolInput.value.toUpperCase()
}


</script>

<style scoped>
ul {
  margin-top: 4px;
  background: #eee;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5em;
}
li:hover {
  background: #ddd;
}
.chart-box {
  margin-top: 2em;
  max-width: 400px;
}
</style>
