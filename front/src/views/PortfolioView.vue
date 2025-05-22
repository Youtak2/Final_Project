<template>
  <div class="portfolio-container">
    <h3>포트폴리오 수정</h3>

    <div class="info-row">
      <label>저축 성향</label>
      <div class="checkbox-group">
        <label><input type="radio" value="소극적" v-model="portfolio.saving_type" /> 소극적</label>
        <label><input type="radio" value="중립적" v-model="portfolio.saving_type" /> 중립적</label>
        <label><input type="radio" value="적극적" v-model="portfolio.saving_type" /> 적극적</label>
      </div>
    </div>

    <div class="info-row">
      <label>투자 성향</label>
      <div class="checkbox-group">
        <label><input type="radio" value="안정형" v-model="portfolio.invest_type" /> 안정형</label>
        <label><input type="radio" value="위험중립형" v-model="portfolio.invest_type" /> 위험중립형</label>
        <label><input type="radio" value="공격투자형" v-model="portfolio.invest_type" /> 공격투자형</label>
      </div>
    </div>

    <div class="info-row">
      <label>주거래 은행</label>
      <select v-model="portfolio.main_bank">
        <option disabled value="">선택하세요</option>
        <option v-for="bank in bankOptions" :key="bank" :value="bank">{{ bank }}</option>
      </select>
    </div>

    <button @click="savePortfolio">저장하기</button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'

const portfolio = reactive({
  saving_type: '',
  invest_type: '',
  main_bank: ''
})

const bankOptions = [
  '경남은행', '광주은행', '국민은행', '농협은행', '대구은행',
  '부산은행', '수협은행', '신한은행', '우리은행', '전북은행',
  '제주은행', '카카오뱅크', '케이뱅크', 'IBK 기업은행',
  '토스뱅크', '하나은행', '한국산업은행', '한국 스탠다드은행'
]

async function savePortfolio() {
  const token = localStorage.getItem('token')
  try {
    await axios.patch('http://127.0.0.1:8000/api/v1/accounts/portfolio/', portfolio, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    alert('포트폴리오 저장 완료!')
  } catch (err) {
    console.error('저장 실패:', err)
    alert('저장 실패!')
  }
}
</script>

<style scoped>
.portfolio-container {
  max-width: 600px;
  margin: auto;
  background: #fff;
  padding: 2rem;
  border-radius: 10px;
}
.info-row {
  margin-bottom: 1rem;
}
.checkbox-group {
  display: flex;
  gap: 1rem;
}
select {
  padding: 0.5rem;
}
</style>
