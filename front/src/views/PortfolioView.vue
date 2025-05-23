<template>
  <div class="portfolio-container">
    <h3>포트폴리오 수정</h3>

    <!-- 저축 성향 -->
    <div class="section">
      <label>저축 성향</label>
      <div class="button-group">
        <button
          v-for="type in savingTypes"
          :key="type"
          :class="{ active: portfolio.saving_type === type }"
          @click="portfolio.saving_type = type"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <!-- 투자 성향 -->
    <div class="section">
      <label>투자 성향</label>
      <div class="button-group">
        <button
          v-for="type in investTypes"
          :key="type"
          :class="{ active: portfolio.invest_type === type }"
          @click="portfolio.invest_type = type"
        >
          {{ type }}
        </button>
      </div>
    </div>

    <!-- 주거래 은행 -->
    <div class="section">
      <label>주거래 은행</label>
      <select v-model="portfolio.main_bank">
        <option disabled value="">선택하세요</option>
        <option v-for="bank in bankOptions" :key="bank" :value="bank">
          {{ bank }}
        </option>
      </select>
    </div>

    <button class="save-btn" @click="savePortfolio">저장하기</button>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import axios from 'axios'

const portfolio = reactive({
  saving_type: '',
  invest_type: '',
  main_bank: ''
})

const savingTypes = ['소극적', '중립적', '적극적']
const investTypes = ['안정형', '위험중립형', '공격투자형']
const bankOptions = [
  '경남은행', '광주은행', '국민은행', '농협은행', '대구은행',
  '부산은행', '수협은행', '신한은행', '우리은행', '전북은행',
  '제주은행', '카카오뱅크', '케이뱅크', 'IBK 기업은행',
  '토스뱅크', '하나은행', '한국산업은행', '한국 스탠다드은행'
]

const token = localStorage.getItem('token')

async function fetchPortfolio() {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/portfolio/', {
      headers: { Authorization: `Token ${token}` }
    })
    Object.assign(portfolio, res.data)
  } catch (err) {
    console.error('불러오기 실패:', err)
  }
}

async function savePortfolio() {
  try {
    await axios.patch('http://127.0.0.1:8000/api/v1/accounts/portfolio/', portfolio, {
      headers: { Authorization: `Token ${token}` }
    })
    alert('포트폴리오 저장 완료!')
  } catch (err) {
    console.error('저장 실패:', err)
    alert('저장 실패!')
  }
}

onMounted(fetchPortfolio)
</script>

<style scoped>
.portfolio-container {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.section {
  margin-bottom: 1.5rem;
}

.button-group {
  display: flex;
  gap: 0.8rem;
  margin-top: 0.5rem;
}

.button-group button {
  padding: 0.6rem 1.2rem;
  border: 1px solid #ddd;
  background: #f8f8f8;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.button-group button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.save-btn {
  background-color: #28a745;
  color: white;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

select {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 0.5rem;
}
</style>
