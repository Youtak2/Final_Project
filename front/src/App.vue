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
        <RouterLink to="/deposit">예적금 금리 비교</RouterLink>
        <RouterLink to="/etf">현물 상품 비교</RouterLink>
        <RouterLink to="/bank-search">근처 은행 검색</RouterLink>
        <RouterLink to="/invest">투자정보</RouterLink>
        <RouterLink to="/lounge">금융상품 추천</RouterLink>
        <RouterLink to="/notice">공지/공시</RouterLink>
        <RouterLink to="/community/articles">커뮤니티</RouterLink>
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
const showDropdown = ref(false)

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

<style>
/* ✅ scoped 제거됨 - 전역 스타일로 적용됨 */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

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
</style>
