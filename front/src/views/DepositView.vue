<template>
  <v-container>
    <ViewTitle 
      title="예적금 금리 비교" 
      subtitle="최적의 금융상품을 한눈에 비교해 보세요"
    />
    <v-card class="pa-4">
      <FinancialProductFilter
        :products="financeStore.financialProducts"
        @update:filters="updateFilters"
        @update:selectedTerm="updateSelectedTerm"
      />
      
      <FinancialProductTable
        :filters="filters"
        :selectedTerm="selectedTerm"
      />
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useFinanceStore } from '@/stores/financialProduct'
import FinancialProductFilter from '@/components/finance/FinancialProductFilter.vue'
import FinancialProductTable from '@/components/finance/FinancialProductTable.vue'
import ViewTitle from '@/components/common/ViewTitle.vue'
const financeStore = useFinanceStore()
const filters = ref({
  bank: null,
  term: null,
  category: null
})
const selectedTerm = ref(null)

const updateFilters = (newFilters) => {
  filters.value = newFilters
}

const updateSelectedTerm = (term) => {
  selectedTerm.value = term
}

// 컴포넌트 마운트 시 상품 데이터 로드
financeStore.getFinancialProducts()
</script>

<style scoped>

</style>