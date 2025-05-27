<template>
  <div class="news-wrapper">
    <div class="center-container" data-aos="fade-up">
      <h2 class="page-title" data-aos="fade-up">📰 한 입 뉴스 요약</h2>

      <div class="search-section" data-aos="fade-up" data-aos-delay="100">
        <div class="autocomplete-area">
          <div class="autocomplete-wrapper">
            <input v-model="symbolInput" placeholder="종목명 입력 (ex: apple, AAPL)" />
            <button @click="search" :disabled="loading">요약 시작</button>
          </div>
          <ul v-if="symbolInput && filteredTickers.length" class="autocomplete-list">
            <li v-for="item in filteredTickers" :key="item.symbol" @click="selectTicker(item)">
              {{ item.name }} ({{ item.symbol }})
            </li>
          </ul>
        </div>
      </div>

      <div v-if="loading" class="loading-message">
        <img src="/video/Loading.gif" alt="로딩 중..." class="loading-gif" />
        <p style="text-align: center; color: #3B82F6;">🔄 뉴스를 불러오는 중입니다...</p>
      </div>

      <div v-if="results.length" class="result-area">
        
        <div class="favorite-wrapper">
          <FavoriteButton :symbol="selectedSymbol" />
        </div>

        <div class="chart-box">
          <h3>📊 감성 분석 통계</h3>
          <canvas id="sentimentChart"></canvas>
        </div>
        
        <h3>📋 요약 결과</h3>
        <ul class="summary-list">
          <li :class="['news-card', impactClass(r.impact)]" v-for="r in results" :key="r.link">
            <h4 class="news-title">{{ r.title }} <span class="impact">- {{ r.impact }}</span></h4>
            <p class="news-summary">{{ r.translated_summary }}</p>
            <a :href="r.link" target="_blank" class="news-link">🔗 원문 보기</a>
          </li>
        </ul>
  
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import tickers from '../assets/tickers.json'
import FavoriteButton from '../components/FavoriteButton.vue'

const symbolInput = ref('')
const selectedSymbol = ref('')
const loading = ref(false)
const results = ref([])
const isLoading = computed(() => loading.value)
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
}

const renderChart = async () => {
  try {
    const res = await axios.get(`/api/v1/news/sentiment-stats/?symbol=${selectedSymbol.value}`);
    const counts = res.data.sentiment;

    const ctx = document.getElementById('sentimentChart');
    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: Object.keys(counts),
        datasets: [{
          data: Object.values(counts),
          backgroundColor: ['#4caf50', '#f44336', '#9e9e9e', '#cccccc']
        }]
      }
    });
  } catch (err) {
    console.error("감성 통계 로딩 실패", err);
  }
};


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

const impactClass = (impact) => {
  const base = (impact || '').toString().trim().replace(/\s/g, '');

  if (base.includes('긍정')) return 'impact-positive';
  if (base.includes('부정')) return 'impact-negative';
  if (base.includes('중립')) return 'impact-neutral';
  return 'impact-etc';
};


</script>

<style scoped>
:root {
  --blue-dark: #1E3A8A;
  --blue-main: #3B82F6;
  --gray-border: #E5E7EB;
}

.news-wrapper {
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

.page-title {
  font-size: 1.6rem;
  color: var(--blue-dark);
  font-weight: 700;
  margin-bottom: 1.5rem;
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
  gap: 10px;
  justify-content: center;
}

input {
  width: 300px;
  padding: 10px 12px;
  border: 1px solid var(--gray-border);
  border-radius: 8px;
  font-size: 1rem;
}

button {
  padding: 10px 16px;
  background-color: var(--blue-main);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: 0.2s;
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
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-top: 4px;
}
.autocomplete-list li {
  padding: 8px 12px;
  cursor: pointer;
}
.autocomplete-list li:hover {
  background: #f0f4ff;
}

.result-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.summary-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}
.summary-list li {
  padding: 1rem;
  background: #f9fafb;
  border: 1px solid var(--gray-border);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.summary-list strong {
  color: var(--blue-dark);
}

.chart-box {
  max-width: 400px;
  margin: 2rem auto;
}

.loading-gif {
  width: 200px;
  height: auto;
  display: block;
  margin: 0 auto;
}

.favorite-wrapper {
  width: 100%;
  max-width: 400px;
  margin: 1rem auto;
}

.news-card {
  background-color: #ffffff;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
.news-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.news-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #1E3A8A;
  margin-bottom: 0.5rem;
}

.impact {
  font-size: 0.95rem;
  color: #555;
}

.news-summary {
  font-size: 0.95rem;
  margin-bottom: 0.8rem;
  line-height: 1.4;
}

.news-link {
  color: #3B82F6;
  font-weight: bold;
  text-decoration: none;
}
.news-link:hover {
  text-decoration: underline;
}
.impact-positive {
  border-color: #4caf50; /* 초록 */
}

.impact-negative {
  border-color: #f44336; /* 빨강 */
}

.impact-neutral {
  border-color: #9e9e9e; /* 회색 */
}

.impact-etc {
  border-color: #cccccc; /* 기타 */
}
</style>
