<template>
  <section class="hero">
    <div class="hero-inner">
      <h1 class="hero-title">StockBite, 해외 투자를 한 입에</h1>
      <p class="hero-subtitle">예적금, 주식, 추천까지. 어렵고 귀찮은 금융, StockBite로 한번에 끝내요.</p>
      <div class="hero-buttons">
        <RouterLink to="/deposit" class="btn btn-primary">예적금 금리 비교</RouterLink>
        <RouterLink to="/recommend" class="btn btn-secondary">퀀텀 추천 종목</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background-color: white;
  padding: 6rem 1rem 5rem;
  text-align: center;
  border-bottom: 1px solid var(--line-gray);
}

.hero-inner {
  max-width: 960px;
  margin: 0 auto;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--blue-dark);
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: var(--gray-text);
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  letter-spacing: -0.01em;
}


.btn-primary {
  background-color: var(--blue-main);
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: var(--orange-main);
  color: white;
}

.btn-secondary:hover {
  background-color: #ea580c;
}
</style>
