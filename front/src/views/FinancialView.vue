<template>
  <div>
    <input v-model="query" @keyup.enter="search" placeholder="종목명 또는 티커 입력" />

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
            <td>{{ row }}</td>
            <td v-for="col in columns" :key="col">{{ financials[col][row] || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const symbol = ref('')
const financials = ref(null)
const columns = ref([])
const rows = ref([])


function search() {
  symbol.value = query.value.toUpperCase()
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

</script>
