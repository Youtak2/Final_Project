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
        <RouterLink to="/deposit">예적금 금리 비교</RouterLink>
        <RouterLink to="/stock">현물 상품 비교</RouterLink>
        <RouterLink to="/bank-search">근처 은행 검색</RouterLink>
        <RouterLink to="/financial">투자 정보</RouterLink>
        <RouterLink to="/news-summary">투자 뉴스</RouterLink>
        <RouterLink to="/recommend">종목 추천</RouterLink>
        <RouterLink to="/community/articles">커뮤니티</RouterLink>
        <RouterLink v-if="isLogin" to="/simulation">가상 포트폴리오</RouterLink>
      </nav>

     <div class="nav-icons">
        <!-- <input type="text" placeholder="검색..." class="search-input" />
        <span class="icon">🔍</span> -->

        <!-- 로그인 상태별 분기 -->
        <div v-if="auth.isLogin">
          <RouterLink to="/mypage" class="mypage-link">마이페이지</RouterLink>
          <button @click="logout" class="logout-btn">로그아웃</button>
        </div>
        <div v-else>
          <RouterLink to="/auth" class="mypage-link">로그인</RouterLink>
        </div>

        <div
          class="dropdown-wrapper"
          @mouseover="showDropdown = true"
          @mouseleave="showDropdown = false"
        >
          <span class="icon">≡</span>
          <div class="dropdown-menu" v-if="showDropdown">
            <RouterLink to="/notice">공지사항</RouterLink>
            <RouterLink to="/terms">이용약관</RouterLink>
            <RouterLink to="/community">커뮤니티</RouterLink>
            <RouterLink to="/faq">자주 묻는 질문</RouterLink>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <HeroSection v-if="$route.path === '/'" />
    <ServiceSummary v-if="$route.path === '/'"/>

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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HeroSection from '@/components/HeroSection.vue'
import ServiceSummary from '@/components/ServiceSummary.vue'

const auth = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)

const isLogin = computed(() => auth.isLogin)

// 앱 로드 시 로그인 상태 복원
onMounted(() => {
  if (auth.token && !auth.user) {
    auth.fetchUser()
  }
})

// 로그아웃 함수 수정
const logout = () => {
  auth.logout()  // clearToken → logout 으로 변경
  alert('로그아웃 되었습니다.')
  router.push('/')
}
</script>



<style>
:root {
  --blue-dark: #1E3A8A;
  --blue-main: #3B82F6;
  --red-main: #EF4444;
  --orange-main: #F97316;
  --gray-text: #6B7280;
  --bg-light: #F9FAFB;
  --line-gray: #E5E7EB;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: var(--bg-light);
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 2rem;
  background-color: white;
  border-bottom: 1px solid var(--line-gray);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
  flex-wrap: wrap;
}

.logo img {
  height: 40px;
}

.nav {
  display: flex;
  flex: 1;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.nav a {
  color: var(--blue-dark);
  font-weight: 500;
  font-size: 1rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.nav a:hover {
  color: var(--blue-main);
}

/* Icons and Auth */
.nav-icons {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: 1.2rem;
  color: var(--gray-text);
}

.search-input {
  padding: 0.4rem 0.6rem;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.mypage-link,
.login-link {
  font-size: 0.9rem;
  color: var(--blue-dark);
  text-decoration: none;
}

.logout-btn {
  font-size: 0.9rem;
  color: var(--red-main);
  background: transparent;
  border: none;
  cursor: pointer;
}

/* Dropdown */
.dropdown-wrapper {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 120%;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  z-index: 999;
  min-width: 150px;
  display: flex;
  flex-direction: column;
}

.dropdown-menu a {
  text-decoration: none;
  color: #333;
  padding: 0.5rem 0;
  font-size: 0.9rem;
}

.dropdown-menu a:hover {
  background-color: #f5f5f5;
}

/* Main */
main {
  flex: 1;
  padding: 4rem 1rem;
  max-width: 960px;
  margin: 0 auto;
}

/* Footer */
.footer {
  text-align: center;
  padding: 1.5rem;
  background-color: #f1f1f1;
  font-size: 0.9rem;
  color: #666;
}

</style>
