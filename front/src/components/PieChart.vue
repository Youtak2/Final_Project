<template>
  <div>
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Pie } from 'vue-chartjs'
import {
  Chart,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

// ✅ Chart.js 플러그인 등록
Chart.register(Title, Tooltip, Legend, ArcElement, CategoryScale, ChartDataLabels)

const props = defineProps({
  holdings: {
    type: Array,
    required: true,
  },
})

// ✅ 차트 데이터
const chartData = ref({
  labels: [],
  datasets: [
    {
      label: '투자 비중',
      backgroundColor: [],
      data: [],
    },
  ],
})

// ✅ 차트 옵션
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    // ✅ 내부에 % 표시
    datalabels: {
      formatter: (value, context) => {
        const data = context.chart.data.datasets[0].data
        const total = data.reduce((sum, val) => sum + val, 0)
        const percent = ((value / total) * 100).toFixed(1)
        return `${percent}%`
      },
      color: '#fff',
      font: {
        weight: 'bold',
        size: 14,
        family: 'Pretendard, sans-serif',
      },
    },
    legend: {
      position: 'bottom',
      labels: {
        color: '#1E3A8A',
        font: {
          size: 14,
          family: 'Pretendard, sans-serif',
        },
      },
    },
    title: {
      display: true,
      text: '📊 투자 비중 파이차트',
      color: '#1E3A8A',
      font: {
        size: 18,
        weight: 'bold',
        family: 'Pretendard, sans-serif',
      },
      padding: { bottom: 10 },
    },
  },
}

// ✅ 배경색 랜덤 생성 함수
function generateRandomColor() {
  const r = Math.floor(Math.random() * 200 + 30)
  const g = Math.floor(Math.random() * 200 + 30)
  const b = Math.floor(Math.random() * 200 + 30)
  return `rgba(${r}, ${g}, ${b}, 0.7)`
}

// ✅ 데이터 변경 감지
watch(
  () => props.holdings,
  (newHoldings) => {
    if (!newHoldings || newHoldings.length === 0) {
      chartData.value.labels = []
      chartData.value.datasets[0].data = []
      chartData.value.datasets[0].backgroundColor = []
      return
    }

    const labels = []
    const data = []
    const backgroundColor = []

    newHoldings.forEach((h) => {
      labels.push(h.symbol)
      data.push(Number(h.avg_price) * Number(h.shares))
      backgroundColor.push(generateRandomColor())
    })

    chartData.value = {
      labels,
      datasets: [
        {
          label: '투자 비중',
          backgroundColor,
          data,
        },
      ],
    }
  },
  { immediate: true }
)
</script>

<style scoped>
div {
  max-width: 480px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #f9fafb;
  border-radius: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* 차트 높이 제한 */
canvas {
  max-height: 320px !important;
}
</style>
