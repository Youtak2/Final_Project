<template>
  <button
    class="favorite-button"
    @click="toggleFavorite"
    :style="{ backgroundColor: isFavorite ? '#ff6b81' : '#f1f2f6' }"
  >
    {{ isFavorite ? '💖 관심 해제' : '🤍 관심 등록' }}
  </button>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

// 배포에서 전달된 symbol
const props = defineProps({
  symbol: {
    type: String,
    required: true
  }
})

const isFavorite = ref(false)

const checkFavoriteStatus = async () => {
  const token = localStorage.getItem('token')
  if (!token || !props.symbol) {
    isFavorite.value = false
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/favorites/', {
      headers: { Authorization: `Token ${token}` }
    })
    isFavorite.value = res.data.some(item => item.symbol === props.symbol)
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
        data: { symbol: props.symbol }
      })
      isFavorite.value = false
    } else {
      await axios.post('http://127.0.0.1:8000/api/v1/accounts/favorites/',
        { symbol: props.symbol },
        { headers })
      isFavorite.value = true
    }
  } catch (err) {
    console.error('찜 처리 실패:', err)
  }
}

onMounted(checkFavoriteStatus)
watch(() => props.symbol, checkFavoriteStatus)
</script>

<style scoped>
.favorite-button {
  width: 100%;   /* ✅ 부모로부터 전체 너비 상속 */
  padding: 10px;
  background-color: #f87171;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: bold;
  font-size: 0.75rem;
  transition: 0.2s;
  cursor: pointer;
  padding: 0.3rem 0.6rem;
  text-overflow: ellipsis;
  overflow: hidden;
  max-width: 110px; 
  white-space: nowrap;
}
.favorite-button:hover {
  background-color: #ef4444;
  opacity: 0.9;
}
</style>
