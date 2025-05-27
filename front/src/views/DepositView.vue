<template>
  <div class="deposit-container">
    <h2 data-aos="fade-up">💰 가장 맛있는 금리 보기</h2>
    <SummaryCard v-if="avgRate !== undefined && maxRate !== undefined" :avg="avgRate" :max="maxRate" />

    
    <!-- 필터 -->
    <div class="filters" data-aos="fade-up" data-aos-delay="100">
      <select v-model="filters.productType">
        <option value="">상품구분</option>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
      </select>

      <button @click="fetchProducts">조회</button>

      <label class="bookmark-toggle">
        <input type="checkbox" v-model="showBookmarksOnly" />
        찜한 상품만 보기
      </label>
    </div>

    <!-- 은행 체크박스 -->
    <div class="bank-checkboxes" data-aos="fade-up" data-aos-delay="200">
      <label v-for="bank in bankList" :key="bank">
        <input type="checkbox" :value="bank" v-model="filters.banks" />
        {{ bank }}
      </label>
    </div>



    <!-- 금리 테이블 -->
    <div class="table-wrapper">
      <table data-aos="fade-up" data-aos-delay="300">
        <thead>
          <tr>
            <th> </th>
            <th>공시 제출월</th>
            <th>금융회사</th>
            <th>상품명</th>
            <th @click="toggleSort('rate_6')">
              6개월 금리
              <span v-if="sortKey === 'rate_6'">{{ sortDesc ? '⬇️' : '⬆️' }}</span>
            </th>
            <th @click="toggleSort('rate_12')">
              12개월 금리
              <span v-if="sortKey === 'rate_12'">{{ sortDesc ? '⬇️' : '⬆️' }}</span>
            </th>
            <th @click="toggleSort('rate_24')">
              24개월 금리
              <span v-if="sortKey === 'rate_24'">{{ sortDesc ? '⬇️' : '⬆️' }}</span>
            </th>
            <th @click="toggleSort('rate_36')">
              36개월 금리
              <span v-if="sortKey === 'rate_36'">{{ sortDesc ? '⬇️' : '⬆️' }}</span>
            </th>
            <th> </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedItems" :key="item.name + item.bank_name">
            <td>
              <img
                :src="`/logos/${item.bank_name}.png`"
                alt="logo"
                class="bank-logo"
                @error="handleLogoError"
              />
            </td>
            <td>{{ item.disclosure_month }}</td>
            <td v-html="formatBankName(item.bank_name)"></td>
            <td>
              <RouterLink :to="`/deposit/${item.id}`">{{ item.name }}</RouterLink>
            </td>
            <td>{{ item.rate_6 ?? '-' }}</td>
            <td>{{ item.rate_12 ?? '-' }}</td>
            <td>{{ item.rate_24 ?? '-' }}</td>
            <td>{{ item.rate_36 ?? '-' }}</td>
            <td>
              <button @click="toggleBookmark(item.id)">
                <span v-if="bookmarkedIds && bookmarkedIds.includes(item.id)">💖</span>
                <span v-else>🤍</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- 페이지네이션 -->
    <div class="pagination" data-aos="fade-up" data-aos-delay="400">
      <label>페이지당 항목 수:
        <select v-model="itemsPerPage">
          <option :value="10">10</option>
          <option :value="20">20</option>
        </select>
      </label>
      {{ currentPage }} / {{ totalPages }}
      <button :disabled="currentPage === 1" @click="currentPage--">←</button>
      <button :disabled="currentPage === totalPages" @click="currentPage++">→</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import SummaryCard from '@/components/SummaryCard.vue'


const filters = ref({
  productType: '',
  banks: [],
})

const allItems = ref([])
const bankList = ref([])
const itemsPerPage = ref(10)
const currentPage = ref(1)
const sortKey = ref('rate_12') // 기본 정렬 기준
const sortDesc = ref(true)
const showBookmarksOnly = ref(false)

const fetchProducts = async () => {
  const allRes = await axios.get('http://127.0.0.1:8000/api/v1/deposit/products/')
  const banks = new Set(allRes.data.map(item => item.bank_name))
  bankList.value = Array.from(banks).sort()

  const res = await axios.get('http://127.0.0.1:8000/api/v1/deposit/products/', {
    params: {
      productType: filters.value.productType,
      bank: filters.value.banks,
    },
    paramsSerializer: params => {
      const query = new URLSearchParams()
      for (const key in params) {
        if (Array.isArray(params[key])) {
          params[key].forEach(val => query.append(key, val))
        } else if (params[key]) {
          query.append(key, params[key])
        }
      }
      return query.toString()
    }
  })

  allItems.value = res.data
  currentPage.value = 1
}

const filteredItems = computed(() => {
  return showBookmarksOnly.value
    ? allItems.value.filter(i => bookmarkedIds.value.includes(i.id))
    : allItems.value
})

const sortedItems = computed(() => {
  return [...filteredItems.value].sort((a, b) => {
    const aVal = a[sortKey.value] || 0
    const bVal = b[sortKey.value] || 0
    return sortDesc.value ? bVal - aVal : aVal - bVal
  })
})


const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return sortedItems.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => Math.ceil(sortedItems.value.length / itemsPerPage.value))

onMounted(fetchProducts)



const bookmarkedIds = ref([])

const loadBookmarks = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  const res = await axios.get('http://127.0.0.1:8000/api/v1/deposit/bookmark/list/', {
    headers: { Authorization: `Token ${token}` }
  })
  bookmarkedIds.value = res.data.map(b => b.product)  // ✅ id만 추출
}

onMounted(() => {
  fetchProducts()
  loadBookmarks()
})

const toggleBookmark = async (productId) => {
  console.log("📌 Bookmark 요청할 productId:", productId)
  const token = localStorage.getItem('token')

  if (!token) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/deposit/bookmark/', {
      product_id: productId
    }, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    if (res.data.bookmarked) {
      bookmarkedIds.value.push(productId)
      alert('찜 완료!')
    } else {
      bookmarkedIds.value = bookmarkedIds.value.filter(id => id !== productId)
      alert('찜 해제!')
    }
  } catch (err) {
    alert('요청 실패: 로그인 또는 서버 문제입니다.')
  }
}

// 키워드 기준 줄바꾸기
const formatBankName = (name) => {
  // 1. "주식회사"가 앞에 붙은 경우 → "주식회사<br>나머지"
  if (name.startsWith('주식회사')) {
    return `주식회사<br>${name.slice(4)}`
  }

  // 2. "주식회사"가 뒤에 있는 경우 → 앞부분 + <br> + "주식회사"
  if (name.endsWith('주식회사')) {
    return `${name.replace('주식회사', '')}<br>주식회사`
  }

  // 3. 그 외: 길이 기준 강제 줄바꿈
  if (name.length > 10) {
    return `${name.slice(0, 6)}<br>${name.slice(6)}`
  }

  return name
}

// 예적금 요약
const avgRate = computed(() => {
  const values = sortedItems.value.map(i => i[sortKey.value]).filter(v => v)
  const sum = values.reduce((acc, val) => acc + val, 0)
  return values.length ? sum / values.length : 0
})

const maxRate = computed(() => {
  const valid = sortedItems.value.filter(i => i[sortKey.value])
  if (!valid.length) return { name: '-', rate: 0 }
  const maxItem = valid.reduce((max, item) => item[sortKey.value] > max[sortKey.value] ? item : max)
  return { name: maxItem.name, rate: maxItem[sortKey.value] }
})

// 정렬방향 아이콘 구현
const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortDesc.value = !sortDesc.value
  } else {
    sortKey.value = key
    sortDesc.value = true
  }
}

// 로고 없는 경우 공백 처리
const handleLogoError = (event) => {
  event.target.src = '/logos/default.png' // 혹은 공백 처리
}

</script>

<style scoped>
.deposit-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 3rem 1rem;
  background-color: var(--bg-light);
  border-radius: 1rem;
}

.deposit-container h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--blue-dark);
  margin-bottom: 2rem;
  text-align: center;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.filters select,
.filters button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--line-gray);
  font-size: 1rem;
  background-color: white;
}

.filters button {
  background-color: var(--blue-main);
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.bank-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.bank-checkboxes label {
  background-color: white;
  border: 1px solid var(--line-gray);
  padding: 0.4rem 0.8rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.bank-checkboxes input[type='checkbox'] {
  margin-right: 0.4rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  table-layout: auto; /* ✅ fixed 대신 auto */
}

th {
  background-color: var(--blue-dark);
  color: white;
  font-weight: 600;
  padding: 0.8rem;
  cursor: pointer;
  white-space: nowrap;      /* ✅ 줄바꿈 방지 */
}

th span {
  margin-left: 4px;
  font-size: 0.85rem;
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid #f1f1f1;
  text-align: center;
}

tr:hover {
  background-color: #f9f9f9;
}

.pagination {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 0.95rem;
}

.pagination button {
  padding: 0.4rem 0.8rem;
  border-radius: 0.5rem;
  border: none;
  background-color: var(--blue-main);
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* ✅ 특정 열에 최소 너비 부여 */
th:nth-child(1),
td:nth-child(1) {
  min-width: 100px;
}
th:nth-child(2),
td:nth-child(2) {
  min-width: 120px;
}
th:nth-child(3),
td:nth-child(3) {
  min-width: 160px;
}
th:nth-child(4),
td:nth-child(4),
th:nth-child(5),
td:nth-child(5),
th:nth-child(6),
td:nth-child(6),
th:nth-child(7),
td:nth-child(7) {
  min-width: 100px;
}

.bookmark-toggle {
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--gray-text);
}

.bank-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.table-wrapper {
  display: flex;
  justify-content: center;
}

</style>
