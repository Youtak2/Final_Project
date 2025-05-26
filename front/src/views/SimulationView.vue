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
            <th>평균 매입가</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="holding in portfolio.holdings" :key="holding.symbol">
            <td>{{ holding.symbol }}</td>
            <td>{{ formatNumber(holding.shares) }}</td>
            <td>{{ formatCurrency(holding.avg_price) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>보유한 종목이 없습니다.</p>
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

const portfolio = ref({})
const auth = useAuthStore()
const tab = ref('holdings')

function formatCurrency(value) {
  const num = Number(value)
  return isNaN(num) ? '...' : num.toFixed(2)
}
function formatNumber(value) {
  const num = Number(value)
  return isNaN(num) ? '-' : num.toFixed(4)
}

async function fetchPortfolio() {
  if (!auth.isAuthenticated) return
  try {
    const res = await api.get('simulation/')
    portfolio.value = res.data
  } catch {
    // 에러 처리 (생략 가능)
  }
}

onMounted(fetchPortfolio)

async function refreshPortfolio() {
  await fetchPortfolio()
  tab.value = 'holdings'  // 매수/매도 후 자동 보유종목 탭 이동
}
</script>

<style scoped>
.portfolio-table {
  border-collapse: collapse;
  width: 100%;
}
.portfolio-table th,
.portfolio-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}
nav button {
  margin-right: 10px;
  padding: 6px 12px;
}
nav button.active {
  background-color: #007bff;
  color: white;
}
</style>
