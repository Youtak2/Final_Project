<template>
  <div>
    <h2>주식 매도</h2>
    <form @submit.prevent="sellStock" autocomplete="off">
      <label>
        종목 코드 (예: AAPL):
        <input
          v-model="searchTerm"
          @input="onInput"
          @keydown.down.prevent="moveDown"
          @keydown.up.prevent="moveUp"
          @keydown.enter.prevent="selectHighlighted"
          required
        />
        <ul v-if="suggestions.length" class="autocomplete-list">
          <li
            v-for="(item, index) in suggestions"
            :key="item.symbol"
            :class="{ highlighted: index === highlightedIndex }"
            @mousedown.prevent="selectSuggestion(item)"
          >
            {{ item.name }} ({{ item.symbol }})
          </li>
        </ul>
      </label>
      <label>
        매도 수량:
        <input type="number" v-model.number="shares" min="1" required />
      </label>
      <button type="submit" :disabled="loading">매도</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/utils/api'
import { useAuthStore } from '@/stores/auth'
import tickerData from '@/assets/tickers.json'  // 종목 데이터 JSON import

const searchTerm = ref('')
const symbol = ref('')  // 실제 요청에 쓸 심볼 저장용
const shares = ref(1)
const message = ref('')
const loading = ref(false)
const auth = useAuthStore()
const emit = defineEmits(['success'])

const suggestions = ref([])
const highlightedIndex = ref(-1)

const onInput = () => {
  const val = searchTerm.value.trim().toLowerCase()
  if (val.length < 1) {
    suggestions.value = []
    return
  }
  suggestions.value = tickerData.filter(
    item =>
      (item.name && item.name.toLowerCase().includes(val)) ||
      (item.symbol && item.symbol.toLowerCase().includes(val))
  ).slice(0, 10)
  highlightedIndex.value = -1
}

const moveDown = () => {
  if (highlightedIndex.value < suggestions.value.length - 1) {
    highlightedIndex.value++
  }
}

const moveUp = () => {
  if (highlightedIndex.value > 0) {
    highlightedIndex.value--
  }
}

const selectHighlighted = () => {
  if (
    highlightedIndex.value >= 0 &&
    highlightedIndex.value < suggestions.value.length
  ) {
    selectSuggestion(suggestions.value[highlightedIndex.value])
  }
}

const selectSuggestion = (item) => {
  searchTerm.value = `${item.symbol}`
  symbol.value = item.symbol
  suggestions.value = []
}

async function sellStock() {
  if (!auth.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!symbol.value) {
    // 자동완성으로 선택 안했으면 입력값을 심볼로 처리해봄
    symbol.value = searchTerm.value.trim().toUpperCase()
  }

  loading.value = true
  message.value = ''
  try {
    const res = await api.post('simulation/sell/', {
      symbol: symbol.value,
      shares: shares.value,
    })
    message.value = res.data.message
    searchTerm.value = ''
    symbol.value = ''
    shares.value = 1

    emit('success')
  } catch (e) {
    message.value = e.response?.data?.error || '매도 실패'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.autocomplete-list {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  max-height: 180px;
  overflow-y: auto;
  width: 100%;
  margin-top: 0;
  padding-left: 0;
  list-style: none;
  z-index: 100;
}
.autocomplete-list li {
  padding: 6px 10px;
  cursor: pointer;
}
.autocomplete-list li.highlighted,
.autocomplete-list li:hover {
  background-color: #e6f0ff;
}
label {
  display: block;
  position: relative;
  margin-bottom: 1rem;
}
</style>
