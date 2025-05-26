<template>
  <div class="favorites-container">
    <h2>📈 관심 종목 목록</h2>
    <ul>
      <li v-for="stock in favorites" :key="stock.symbol">
        {{ stock.symbol }}
        <button @click="removeFavorite(stock.symbol)">삭제</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const favorites = ref([])

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
    headers: { Authorization: `Token ${token}` }
  })
  favorites.value = res.data
})

const removeFavorite = async (symbol) => {
  const token = localStorage.getItem('token')
  await axios.delete('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
    headers: { Authorization: `Token ${token}` },
    data: { symbol }
  })
  favorites.value = favorites.value.filter(s => s.symbol !== symbol)
}
</script>

<style scoped>
.favorites-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  font-family: sans-serif;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 0.5rem 0;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
}
</style>
