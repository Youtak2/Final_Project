<template>
  <v-data-table
    :headers="visibleHeaders"
    :items="filteredProducts"
    :sort-by="sortBy"
    :sort-desc="sortDesc"
    class="elevation-1"
    @click:row="handleRowClick"
  >
    <template v-slot:item.dcls_month="{ item }">
      {{ formatMonth(item.dcls_month) }}
    </template>
  </v-data-table>
</template>

<script setup>
import { useFinanceStore } from '@/stores/financialProduct';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const financeStore = useFinanceStore()
const router = useRouter()

// 테이블 헤더 정의
const headers = [
  { title: '공시 제출월', key: 'dcls_month', sortable: true },
  { title: '금융회사', key: 'kor_co_nm', sortable: true },
  { title: '상품명', key: 'fin_prdt_nm', sortable: true },
  { title: '6개월 금리', key: 'intr_rate_6', sortable: true },
  { title: '12개월 금리', key: 'intr_rate_12', sortable: true },
  { title: '24개월 금리', key: 'intr_rate_24', sortable: true },
  { title: '36개월 금리', key: 'intr_rate_36', sortable: true },
]

// 정렬 상태 관리
const sortBy = ref([])
const sortDesc = ref([])

// 날짜 포맷팅 함수
const formatMonth = (value) => {
  if (!value) return ''
  return `${value.slice(0, 4)}년 ${value.slice(4)}월`
}

// 데이터 가공
const processedProducts = computed(() => {
  return financeStore.financialProducts.map(product => {
    // 기본 상품 정보
    const baseInfo = {
      unique_id: product.unique_id,
      category: product.category,
      dcls_month: product.dcls_month,
      kor_co_nm: product.kor_co_nm,
      fin_prdt_nm: product.fin_prdt_nm,
      intr_rate_6: '-',
      intr_rate_12: '-',
      intr_rate_24: '-',
      intr_rate_36: '-'
    }

    // 옵션에서 각 기간별 금리 정보 추출
    product.options?.forEach(opt => {
      switch (opt.save_trm) {
        case 6:
          baseInfo.intr_rate_6 = opt.intr_rate
          break
        case 12:
          baseInfo.intr_rate_12 = opt.intr_rate
          break
        case 24:
          baseInfo.intr_rate_24 = opt.intr_rate
          break
        case 36:
          baseInfo.intr_rate_36 = opt.intr_rate
          break
      }
    })

    return baseInfo
  })
})

const props = defineProps({
  selectedTerm: {
    type: Number,
    default: null
  },
  filters: {
    type: Object,
    default: () => ({
      bank: null,
      term: null,
      category: null
    })
  }
})

// 보이는 헤더 계산
const visibleHeaders = computed(() => {
  if (!props.selectedTerm) return headers

  return headers.filter(header => {
    if (!header.key.startsWith('intr_rate_')) return true
    const termNumber = parseInt(header.key.split('_')[2])
    return termNumber === props.selectedTerm
  })
})

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  return processedProducts.value.filter(product => {
    const bankMatch = !props.filters.bank || product.kor_co_nm === props.filters.bank
    const categoryMatch = !props.filters.category || product.category === props.filters.category
    return bankMatch && categoryMatch
  })
})

const handleRowClick = (event, product) => {
  router.push({
    name: 'FinancialProductDetail',
    params: { productUniqueId: product.item.unique_id }
  })
}

</script>