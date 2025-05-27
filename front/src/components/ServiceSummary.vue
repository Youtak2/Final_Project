<template>
  <section class="summary-section">
    <h2 class="summary-title">💡 어떤 서비스를 제공하나요?</h2>
    <div class="summary-cards">
      <div class="card" data-aos="fade-up">
        <h3>📊 예적금 금리 비교</h3>
        <p>다양한 금융사의 금리를 한눈에 비교해 당신에게 가장 유리한 상품을 찾아보세요.</p>
      </div>
      <div class="card" data-aos="fade-up" data-aos-delay="100">
        <h3>🤖 종목 추천 & 분석</h3>
        <p>퀀텀 알고리즘 기반으로 수익이 기대되는 우량 종목을 추천하고 핵심 재무정보를 분석합니다.</p>
      </div>
      <div class="card" data-aos="fade-up" data-aos-delay="200">
        <h3>🗞️ 투자 뉴스 요약</h3>
        <p>종목 관련 최신 뉴스를 AI로 요약해 바쁜 당신도 빠르게 이슈를 확인할 수 있어요.</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.summary-section {
  padding: 4rem 1rem;
  background-color: var(--bg-light);
  text-align: center;
  border-top: 1px solid var(--line-gray);
}

.summary-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--blue-dark);
  margin-bottom: 2.5rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 960px;
  margin: 0 auto;
}

.card {
  background-color: white;
  border: 1px solid var(--line-gray);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.card h3 {
  font-size: 1.2rem;
  color: var(--blue-main);
  margin-bottom: 1rem;
}

.card p {
  font-size: 0.95rem;
  color: var(--gray-text);
}
</style>
