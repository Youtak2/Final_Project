<template>
  <div class="summary-stats" data-aos="fade-up">
    <div class="summary-item">
      📈 평균 금리: {{ safeAvg }}%
    </div>
    <div class="summary-item">
      🏆 최고 금리: {{ max?.name || '-' }} ({{ max?.rate ?? 0 }}%)
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue' 
const props = defineProps({
  avg: Number,
  max: Object
})

const safeAvg = computed(() => {
  return typeof props.avg === 'number' ? props.avg.toFixed(2) : '0.00'
})
</script>

<style scoped>
.summary-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--blue-dark);
}

.summary-item {
  background: #f1f5ff;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
}
</style>
