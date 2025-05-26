<template>
  <div>
    <h2>주식 매수</h2>
    <form @submit.prevent="buyStock" autocomplete="off" style="position: relative;">
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
        매수 수량:
        <input type="number" v-model.number="shares" min="1" required />
      </label>
      <button type="submit" :disabled="loading">
        {{ loading ? '매수 중...' : '매수' }}
      </button>
    </form>
    <p :class="messageClass" v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '@/utils/api'
import { useAuthStore } from '@/stores/auth'
import tickerData from '@/assets/tickers.json'  // 종목 JSON 파일 임포트

const searchTerm = ref('')
const symbol = ref('')  // 실제 API 호출용 심볼 저장 변수
const shares = ref(1)
const message = ref('')
const loading = ref(false)
const auth = useAuthStore()
const emit = defineEmits(['success'])

const messageClass = computed(() => {
  if (!message.value) return ''
  return message.value.includes('실패') || message.value.includes('오류') ? 'error' : 'success'
})

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

async function buyStock() {
  if (!auth.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!symbol.value) {
    symbol.value = searchTerm.value.trim().toUpperCase()
  }

  const sym = symbol.value.trim().toUpperCase()
  if (!/^[A-Z0-9]+$/.test(sym)) {
    message.value = '종목 코드는 영문자와 숫자만 가능합니다.'
    return
  }
  if (shares.value <= 0 || !Number.isInteger(shares.value)) {
    message.value = '매수 수량은 1 이상의 정수여야 합니다.'
    return
  }

  loading.value = true
  message.value = ''
  try {
    const res = await api.post('simulation/buy/', {
      symbol: symbol.value,
      shares: shares.value,
    })
    message.value = res.data.message
    searchTerm.value = ''
    symbol.value = ''
    shares.value = 1

    emit('success')  // 부모 컴포넌트에 성공 알림
  } catch (e) {
    message.value = e.response?.data?.error || e.message || '매수 실패'
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
.error {
  color: red;
}
.success {
  color: green;
}
</style>
