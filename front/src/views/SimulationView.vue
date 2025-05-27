<template>
  <div>
    <h1>가상 포트폴리오</h1>
    <p>잔액: {{ formatCurrency(portfolio.cash_balance) }} USD</p>

    <nav>
      <button @click="tab = 'holdings'" :class="{ active: tab === 'holdings' }">보유 종목</button>
      <button @click="tab = 'buy'" :class="{ active: tab === 'buy' }">주식 매수</button>
      <button @click="tab = 'sell'" :class="{ active: tab === 'sell' }">주식 매도</button>
    </nav>

    <section v-if="tab === 'holdings'">
      <table v-if="portfolio.holdings && portfolio.holdings.length > 0" class="portfolio-table">
        <thead>
          <tr>
            <th>종목명</th>
            <th>보유 수량</th>
            <th>수익률</th>
            <th>평균 매입가</th>
            <th>현재가</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="holding in portfolio.holdings" :key="holding.symbol">
            <td>{{ holding.symbol }}</td>
            <td>{{ formatNumber(holding.shares) }}</td>
            <td>
              {{ formatPercent((currentPrices[holding.symbol] - holding.avg_price) / holding.avg_price) }}
            </td>
            <td>{{ formatCurrency(holding.avg_price) }}</td>
            <td>{{ formatCurrency(currentPrices[holding.symbol]) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>보유한 종목이 없습니다.</p>

      <div v-if="portfolio.holdings && portfolio.holdings.length > 0" style="max-width: 500px; margin-top: 2rem;">
        <PieChart :holdings="portfolio.holdings" />
      </div>
    </section>

    <section v-if="tab === 'buy'">
      <BuyStock @success="refreshPortfolio" />
    </section>

    <section v-if="tab === 'sell'">
      <SellStock @success="refreshPortfolio" />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { useAuthStore } from '@/stores/auth'
import BuyStock from '@/components/BuyStock.vue'
import SellStock from '@/components/SellStock.vue'
import PieChart from '@/components/PieChart.vue'
import { fetchCurrentPrices } from '@/api/simulation'

const portfolio = ref({})
const auth = useAuthStore()
const tab = ref('holdings')
const currentPrices = ref({})

function formatCurrency(value) {
  const num = Number(value)
  return isNaN(num) ? '...' : num.toFixed(2)
}
function formatNumber(value) {
  const num = Number(value)
  return isNaN(num) ? '-' : num.toFixed(4)
}

async function fetchPortfolio() {
  try {
    const res = await api.get('simulation/')
    portfolio.value = res.data
    await loadPrices()  // ✅ 현재가도 함께 불러옴
  } catch (err) {
    console.error('❌ portfolio 요청 실패', err)
  }
}

onMounted(() => {
  console.log('auth.token:', auth.token)
  console.log('👉 백엔드 요청 시도: http://localhost:8000/api/v1/simulation/')
  fetchPortfolio()
})

async function refreshPortfolio() {
  await fetchPortfolio()
  tab.value = 'holdings'  // 매수/매도 후 자동 보유종목 탭 이동
}


// 실시간 현재가 가져오기
async function loadPrices() {
  if (!portfolio.value.holdings) return
  const symbols = portfolio.value.holdings.map(h => h.symbol)
  currentPrices.value = await fetchCurrentPrices(symbols)
}

// 수익률
function formatPercent(value) {
  if (value === null || value === undefined || isNaN(value)) return '-'
  return (value * 100).toFixed(2) + '%'
}

</script>

<style scoped>
h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #1E3A8A;
}

p {
  text-align: center;
  font-size: 1rem;
  color: #374151;
  margin-bottom: 1.5rem;
}

/* 탭 버튼 영역 */
nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

nav button {
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  border: 2px solid #1E3A8A;
  background-color: white;
  color: #1E3A8A;
  border-radius: 9999px;
  transition: all 0.3s ease;
}

nav button.active,
nav button:hover {
  background-color: #3B82F6;
  color: white;
  border-color: #3B82F6;
}

/* 테이블 */
.portfolio-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  background-color: white;
  margin-bottom: 2rem;
}

.portfolio-table th {
  background-color: #EFF6FF;
  color: #1E3A8A;
  font-weight: 600;
  padding: 0.75rem;
}

.portfolio-table td {
  padding: 0.75rem;
  text-align: center;
  border-bottom: 1px solid #f1f5f9;
}

/* PieChart 컴포넌트 주변 마진 */
section > div:last-child {
  margin: 0 auto;
  margin-top: 2rem;
  max-width: 500px;
}

/* 반응형 여백 */
@media (max-width: 600px) {
  nav {
    flex-direction: column;
    align-items: center;
  }
}

</style>
