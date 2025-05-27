<template>
  <div class="deposit-container">
    <h2>예적금 금리 비교</h2>

    <!-- 필터 -->
    <div class="filters">
      <select v-model="filters.productType">
        <option value="">상품구분</option>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
      </select>

      <button @click="fetchProducts">조회</button>
    </div>

    <!-- 은행 체크박스 -->
    <div class="bank-checkboxes">
      <label v-for="bank in bankList" :key="bank">
        <input type="checkbox" :value="bank" v-model="filters.banks" />
        {{ bank }}
      </label>
    </div>

    <!-- 금리 테이블 -->
    <table>
      <thead>
        <tr>
          <th>공시 제출월</th>
          <th>금융회사</th>
          <th>상품명</th>
          <th @click="sortKey = 'rate_6'">6개월 금리</th>
          <th @click="sortKey = 'rate_12'">12개월 금리</th>
          <th @click="sortKey = 'rate_24'">24개월 금리</th>
          <th @click="sortKey = 'rate_36'">36개월 금리</th>
          <th>찜하기</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in paginatedItems" :key="item.name + item.bank_name">
          <td>{{ item.disclosure_month }}</td>
          <td>{{ item.bank_name }}</td>
          <td><RouterLink :to="`/deposit/${item.id}`">{{ item.name }}</RouterLink></td>
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

    <!-- 페이지네이션 -->
    <div class="pagination">
      <label>Items per page:
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

const filters = ref({
  productType: '',
  banks: [],
})

const allItems = ref([])
const bankList = ref([])
const itemsPerPage = ref(10)
const currentPage = ref(1)
const sortKey = ref('rate_12') // 기본 정렬 기준

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

const sortedItems = computed(() => {
  return [...allItems.value].sort((a, b) => (b[sortKey.value] || 0) - (a[sortKey.value] || 0))
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


</script>

<style scoped>
.deposit-container {
  padding: 20px;
}

.filters {
  margin-bottom: 10px;
  display: flex;
  gap: 10px;
}

.bank-checkboxes {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
}

th, td {
  border: 1px solid #ccc;
  padding: 6px;
  text-align: center;
  cursor: pointer;
}

th:hover {
  background-color: #f0f0f0;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
