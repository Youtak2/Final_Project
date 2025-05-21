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
        <RouterLink to="/funds">근처 은행 검색</RouterLink>
        <RouterLink to="/invest">투자정보</RouterLink>
        <RouterLink to="/lounge">금융상품 추천</RouterLink>
        <RouterLink to="/notice">공지/공시</RouterLink>
      </nav>
      <div class="nav-icons">
        <RouterLink to="/auth" class="mypage-link">로그인</RouterLink>
        <input type="text" placeholder="검색..." class="search-input" />
        <span class="icon">🔍</span>
        <RouterLink to="/mypage" class="mypage-link">마이페이지</RouterLink>
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
import AuthView from '@/views/AuthView.vue'
</script>

<style scoped>
/* 전체 레이아웃 */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 헤더 */
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 3rem; /* 여유 있는 패딩 */
  background-color: white;
  border-bottom: 1px solid #eaeaea;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 로고 */
.logo img {
  height: 40px;
}

/* 네비게이션 메뉴 */
.nav {
  display: flex;
  flex: 1;
  justify-content: center;
  flex-wrap: wrap;
  gap: 3rem; /* 메뉴 간격 더 넓게 */
}

.nav a {
  color: #111;
  text-decoration: none;
  font-weight: 600;
  font-size: clamp(1rem, 2vw, 1.5rem); /* 더 큰 글씨 */
  white-space: nowrap;
}

/* 아이콘 영역 */
.nav-icons {
  display: flex;
  gap: 1.5rem;
  font-size: 1.8rem; /* 더 큰 아이콘 */
  color: #111;
  cursor: pointer;
  align-items: center;
}

/* 본문 */
main {
  flex: 1;
  padding: 3rem 2rem;
  background-color: #f9fbff;
}

/* 푸터 */
.footer {
  text-align: center;
  padding: 1.5rem;
  background-color: #f1f1f1;
  font-size: 0.9rem;
  color: #666;
}
/* 검색 input */
.search-input {
  padding: 0.4rem 0.6rem;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

/* 마이페이지 링크 */
.mypage-link {
  font-family: "Courier New", Courier, monospace;
  font-size: 0.85rem;
  color: #555;
  text-decoration: none;
  margin-left: 1rem;
}
</style>
