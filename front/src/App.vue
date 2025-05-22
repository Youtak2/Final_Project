<template>
  <div id="app">
    <!-- 헤더 영역 -->
    <header class="header">
      <div class="logo">
        <RouterLink to="/">
          <img src="@/pictures/제목 없음.png" alt="공탁금" />
        </RouterLink>
      </div>
      <nav class="nav">
        <RouterLink to="/">회사소개</RouterLink>
        <RouterLink to="/esg">예적금 금리 비교</RouterLink>
        <RouterLink to="/etf">현물 상품 비교</RouterLink>
        <RouterLink to="/bank-search">근처 은행 검색</RouterLink>
        <RouterLink to="/invest">투자정보</RouterLink>
        <RouterLink to="/lounge">금융상품 추천</RouterLink>
        <RouterLink to="/notice">공지/공시</RouterLink>
      </nav>

      <div class="nav-icons">
        <input type="text" placeholder="검색..." class="search-input" />
        <span class="icon">🔍</span>

        <!-- 로그인 상태별 분기 -->
        <template v-if="isLogin">
          <RouterLink to="/mypage" class="mypage-link">마이페이지</RouterLink>
          <button @click="logout" class="logout-btn">로그아웃</button>
        </template>
        <template v-else>
          <RouterLink to="/auth" class="mypage-link">로그인</RouterLink>
        </template>

        <span class="icon">☰</span>
      </div>
    </header>

    <!-- 본문 -->
    <main>
      <RouterView />
    </main>

    <!-- 푸터 -->
    <footer class="footer">
      <p>ⓒ 공탁금. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isLogin = ref(false)
const router = useRouter()

onMounted(() => {
  isLogin.value = !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  isLogin.value = false
  alert('로그아웃 되었습니다.')
  router.push('/')
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 3rem;
  background-color: white;
  border-bottom: 1px solid #eaeaea;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.logo img {
  height: 40px;
}

.nav {
  display: flex;
  flex: 1;
  justify-content: center;
  flex-wrap: wrap;
  gap: 3rem;
}

.nav a {
  color: #111;
  text-decoration: none;
  font-weight: 600;
  font-size: clamp(1rem, 2vw, 1.5rem);
  white-space: nowrap;
}

.nav-icons {
  display: flex;
  gap: 1.5rem;
  font-size: 1.8rem;
  color: #111;
  cursor: pointer;
  align-items: center;
}

main {
  flex: 1;
  padding: 3rem 2rem;
  background-color: #f9fbff;
}

.footer {
  text-align: center;
  padding: 1.5rem;
  background-color: #f1f1f1;
  font-size: 0.9rem;
  color: #666;
}

.search-input {
  padding: 0.4rem 0.6rem;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.mypage-link {
  font-family: "Courier New", Courier, monospace;
  font-size: 0.85rem;
  color: #555;
  text-decoration: none;
  margin-left: 1rem;
}

.logout-btn {
  background-color: transparent;
  border: none;
  color: #555;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: underline;
}
</style>
