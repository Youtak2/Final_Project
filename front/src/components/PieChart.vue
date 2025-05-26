<template>
  <div>
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Pie } from 'vue-chartjs'
import {
  Chart,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from 'chart.js'

Chart.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

import { computed, watch, ref } from 'vue'

const props = defineProps({
  holdings: {
    type: Array,
    required: true,
  },
})

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

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
    },
    title: {
      display: true,
      text: '투자 비중 파이차트',
    },
  },
}

function generateRandomColor() {
  const r = Math.floor(Math.random() * 200 + 30)
  const g = Math.floor(Math.random() * 200 + 30)
  const b = Math.floor(Math.random() * 200 + 30)
  return `rgba(${r}, ${g}, ${b}, 0.7)`
}

watch(
  () => props.holdings,
  (newHoldings) => {
    if (!newHoldings || newHoldings.length === 0) {
      chartData.value.labels = []
      chartData.value.datasets[0].data = []
      chartData.value.datasets[0].backgroundColor = []
      return
    }

    // 각 종목별 투자 금액 = avg_price * shares
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
