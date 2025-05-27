<template>
  <div class="detail-container" v-if="product">
    <!-- 찜 버튼 -->
    <button type="button" class="bookmark-top" @click="toggleBookmark(product.id)">
      <span v-if="bookmarked">💖</span>
      <span v-else>🤍</span>
    </button>

    <div class="bank-brand" data-aos="fade-up">
      <img :src="`/logos/${product.bank_name}.png`" alt="logo" />
      <span>{{ product.bank_name }}</span>
    </div>

    <div class="info-section" data-aos="fade-up" data-aos-delay="100">
      <h3>📌 상품 정보</h3>
      <p><strong>금융회사:</strong> {{ product.bank_name }}</p>
      <p><strong>상품명:</strong> {{ product.name }}</p>
    </div>

    <div class="info-section" data-aos="fade-up" data-aos-delay="200">
      <h3>💰 금리 정보</h3>
      <p><strong>금리:</strong> {{ product.rate }}%</p>
      <p><strong>저축 기간:</strong> {{ product.save_term }}개월</p>
    </div>
    
    <p><strong>상품 설명:</strong> {{ product.description || '-' }}</p>
    <p><strong>가입 방법:</strong> {{ product.join_way || '-' }}</p>
    <p><strong>가입 대상:</strong> {{ product.join_member || '-' }}</p>

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
  position: relative;
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

.info-section {
  background-color: #f9fafb;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.bank-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}
.bank-brand img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.floating-bookmark {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: white;
  border: 1px solid #ccc;
  padding: 12px 18px;
  border-radius: 50px;
  font-size: 1rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
}


.bookmark-top {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: white;
  border: 1px solid #ccc;
  padding: 6px 12px;
  border-radius: 9999px;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--red-main);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: background-color 0.2s;
  z-index: 10;
}

.bookmark-top:hover {
  background-color: #fef2f2;
}

</style>
