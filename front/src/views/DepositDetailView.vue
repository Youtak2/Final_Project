<template>
  <div class="detail-container" v-if="product">
    <h2>{{ product.name }}</h2>
    <p><strong>금융회사:</strong> {{ product.bank_name }}</p>
    <p><strong>금리:</strong> {{ product.rate }}%</p>
    <p><strong>저축 기간:</strong> {{ product.save_term }}개월</p>
    <p><strong>상품 설명:</strong> {{ product.description || '-' }}</p>
    <p><strong>가입 방법:</strong> {{ product.join_way || '-' }}</p>
    <p><strong>가입 대상:</strong> {{ product.join_member || '-' }}</p>

    <!-- <div v-if="product.join_url">
      <a :href="product.join_url" target="_blank" class="join-btn">👉 가입하러 가기</a>
    </div>
    <p v-else>가입 링크가 제공되지 않습니다.</p> -->

    <!-- 찜 버튼 -->
    <button @click="toggleBookmark(product.id)" class="bookmark-btn">
      <span v-if="bookmarked">💖 찜 해제</span>
      <span v-else>🤍 찜하기</span>
    </button>
  </div>

  <p v-else>로딩 중입니다...</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref(null)
const bookmarked = ref(false)

const fetchProductDetail = async () => {
  const token = localStorage.getItem('token')
  const headers = token ? { Authorization: `Token ${token}` } : {}

  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/deposit/products/${route.params.id}/`, { headers })
    product.value = res.data

    // 찜 여부 확인
    if (token) {
      const bookmarkRes = await axios.get('http://127.0.0.1:8000/api/v1/deposit/bookmark/list/', { headers })
      const ids = bookmarkRes.data.map(b => b.product)
      bookmarked.value = ids.includes(product.value.id)
    }
  } catch (err) {
    console.error('상품 상세 조회 실패:', err)
    alert('상품 정보를 불러오지 못했습니다.')
  }
}

const toggleBookmark = async (productId) => {
  const token = localStorage.getItem('token')
  if (!token) return alert('로그인이 필요합니다.')

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/v1/deposit/bookmark/', {
      product_id: productId
    }, {
      headers: { Authorization: `Token ${token}` }
    })

    bookmarked.value = res.data.bookmarked
    alert(res.data.bookmarked ? '찜 완료!' : '찜 해제!')
  } catch (err) {
    console.error('찜 처리 실패:', err)
    alert('찜 처리 중 오류가 발생했습니다.')
  }
}

onMounted(fetchProductDetail)
</script>

<style scoped>
.detail-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.join-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 10px 20px;
  background-color: #00b894;
  color: white;
  text-decoration: none;
  border-radius: 6px;
}

.bookmark-btn {
  margin-top: 1rem;
  background-color: #f4f4f4;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
