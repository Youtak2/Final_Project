<template>
  <div>
    <input v-model="symbolInput" placeholder="종목명 또는 티커 입력" />
    <ul v-if="symbolInput && filteredTickers.length">
      <li
        v-for="item in filteredTickers"
        :key="item.symbol"
        @click="selectTicker(item)"
        style="cursor: pointer; padding: 2px 0;"
      >
        {{ item.name }} ({{ item.symbol }})
      </li>
    </ul>

    <!-- 이후 검색 버튼 or 자동 로딩으로 조회 -->
    <button @click="load('income')">조회</button>

    <div v-if="symbol">
      <button @click="load('income')">손익계산서</button>
      <button @click="load('balance')">대차대조표</button>
      <button @click="load('cashflow')">현금흐름표</button>

      <table v-if="financials">
        <thead>
          <tr>
            <th>항목</th>
            <th v-for="(col, idx) in columns" :key="idx">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, idx) in rows" :key="idx">
            <!-- 영어 → 한글 번역 -->
            <td>{{ KOREAN_LABELS[row] || row }}</td>
            <td v-for="col in columns" :key="col">
              {{ financials[col][row] || '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>


import { ref, computed } from 'vue'
import axios from 'axios'
import KOREAN_LABELS from '../assets/korean_labels.json'
import tickers from '../assets/tickers.json'

const query = ref('')
const symbol = ref('')
const financials = ref(null)
const columns = ref([])
const rows = ref([])
const symbolInput = ref('')


function search() {
  symbol.value = symbolInput.value.toUpperCase()
  load('income')
}

async function load(type) {
  const res = await axios.get('http://127.0.0.1:8000/api/v1/financial/financials/', {
    params: {
      symbol: symbol.value,
      type: type
    }
    // headers 생략 (AllowAny 덕분에 인증 필요 없음)
  })

  financials.value = res.data
  columns.value = Object.keys(financials.value)
  rows.value = Object.keys(financials.value[columns.value[0]])
}

// 종목 검색 자동완성
const filteredTickers = computed(() => {
  const keyword = symbolInput.value.toLowerCase()
  return tickers.filter(
    item =>
      item.symbol.toLowerCase().includes(keyword) ||
      item.name.toLowerCase().includes(keyword)
  ).slice(0, 5)  // 최대 5개만 표시
})

const selectTicker = (item) => {
  symbolInput.value = `${item.name} (${item.symbol})`
  symbol.value = item.symbol
}

</script>
