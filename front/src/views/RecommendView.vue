<template>
  <div>
    <h2>📊 머신러닝 기반 추천 종목 Top 20</h2>

    <button @click="fetchRecommendations" :disabled="isLoading">
      {{ isLoading ? '🔄 분석 중...' : '🔍 종목 추천 받기' }}
    </button>

    <p v-if="isLoading">🧠 종목 데이터를 분석 중입니다... 잠시만 기다려주세요.</p>

    <table v-if="stocks.length && !isLoading">
      <thead>
        <tr>
          <th>-</th>
          <th>티커</th>
          <th>PER</th>
          <th>ROE</th>
          <th>RSI</th>
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
          <td style="text-align: left;">{{ stock.reason }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!stocks.length && fetchedOnce && !isLoading">
      ⚠️ 추천된 종목이 없습니다.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import FavoriteButton from '../components/FavoriteButton.vue'

const stocks = ref([])
const fetchedOnce = ref(false)
const isLoading = ref(false)

const token = localStorage.getItem('token')

const fetchRecommendations = async () => {
  isLoading.value = true
  stocks.value = []
  fetchedOnce.value = false

  if (!token) {
    alert('로그인이 필요합니다')
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/recommend/', {
      headers: {
        Authorization: `Token ${token}`  // ✅ 반드시 이 헤더 필요
      }
    })
    stocks.value = res.data.top_20
  } catch (err) {
    console.error('API 요청 실패:', err)
  } finally {
    isLoading.value = false
    fetchedOnce.value = true
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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
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
