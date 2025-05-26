<template>
  <div class="mypage-container">
    <h2>내가 찜한 예금 상품 💖</h2>

    <table v-if="bookmarks.length">
      <thead>
        <tr>
          <th>금융회사</th>
          <th>상품명</th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
          <th>-</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in groupedList" :key="item.name + item.bank_name">
          <td>{{ item.bank_name }}</td>
          <td><RouterLink :to="`/deposit/${item.id}`">{{ item.name }}</RouterLink></td>
          <td>{{ item.rate_6 ?? '-' }}</td>
          <td>{{ item.rate_12 ?? '-' }}</td>
          <td>{{ item.rate_24 ?? '-' }}</td>
          <td>{{ item.rate_36 ?? '-' }}</td>
          <td>
            <button @click="toggleBookmark(item)">
              💔 찜 해제
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>찜한 상품이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

// ✅ 상태 선언
const bookmarks = ref([])
const groupedProducts = ref({})
const token = localStorage.getItem('token')

// ✅ 병합된 테이블로 보여줄 배열
const groupedList = computed(() => Object.values(groupedProducts.value))

// ✅ 찜한 상품 불러오기 + 같은 상품군 병합
const fetchBookmarks = async () => {
  groupedProducts.value = {}  // 기존 값 초기화

  const res = await axios.get('http://127.0.0.1:8000/api/v1/deposit/bookmark/list/', {
    headers: { Authorization: `Token ${token}` }
  })

  bookmarks.value = res.data

  for (const bookmark of res.data) {
    const id = bookmark.product_detail.id
    const productGroupRes = await axios.get(`http://127.0.0.1:8000/api/v1/deposit/products/${id}/group/`, {
      headers: { Authorization: `Token ${token}` }
    })

    const group = productGroupRes.data
    if (!group || !group.length) continue

    const p = group[0]  // 대표 상품 정보
    const key = `${p.bank_name}-${p.name}`

    if (!groupedProducts.value[key]) {
      groupedProducts.value[key] = {
        id: p.id,
        bank_name: p.bank_name,
        name: p.name,
        rate_6: null,
        rate_12: null,
        rate_24: null,
        rate_36: null,
      }
    }

    for (const g of group) {
      groupedProducts.value[key][`rate_${g.save_term}`] = g.rate
    }
  }
}

// ✅ 찜 해제 (toggle 방식) → 해제 후 목록 새로고침
const toggleBookmark = async (item) => {
  if (!token) return alert('로그인이 필요합니다.')

  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/deposit/products/`, {
      params: { bank: item.bank_name }
    })

    const group = res.data.filter(p => p.name === item.name)
    for (const product of group) {
      await axios.post('http://127.0.0.1:8000/api/v1/deposit/bookmark/', {
        product_id: product.id
      }, {
        headers: { Authorization: `Token ${token}` }
      })
    }

    alert('찜 해제 완료!')
    await fetchBookmarks()  // ✅ 자동 새로고침
  } catch (err) {
    console.error('찜 해제 실패:', err)
    alert('찜 해제 중 오류 발생')
  }
}

// ✅ 초기 진입 시 찜 목록 불러오기
onMounted(() => {
  if (token) fetchBookmarks()
})
</script>



<style scoped>
.mypage-container {
  max-width: 900px;
  margin: 2rem auto;
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  border: 1px solid #ddd;
  padding: 6px;
  text-align: center;
}
</style>
