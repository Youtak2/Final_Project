<template>
  <v-row class="mb-4">
    <v-col cols="12" md="4">
      <v-select
        v-model="selectedCategory"
        :items="categoryListWithAll"
        label="상품구분"
        variant="outlined"
        density="comfortable"
        bg-color="surface"
        hide-details
        @update:model-value="updateFilters"
      ></v-select>
    </v-col>

    <v-col cols="12" md="4">
      <v-select
        v-model="selectedBank"
        :items="bankListWithAll"
        label="은행 선택"
        variant="outlined"
        density="comfortable"
        bg-color="surface"
        hide-details
        @update:model-value="updateFilters"
      ></v-select>
    </v-col>
    
    <v-col cols="12" md="4">
      <v-select
        v-model="selectedTerm"
        :items="termListWithAll"
        label="예치기간"
        variant="outlined"
        density="comfortable"
        bg-color="surface"
        hide-details
        @update:model-value="updateFilters"
      ></v-select>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  products: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:filters', 'update:selectedTerm'])

const selectedBank = ref('전체')
const selectedTerm = ref('전체')
const selectedCategory = ref('전체')

// 은행 목록
const bankList = computed(() => {
  return [...new Set(props.products.map((item) => item.kor_co_nm))]
})

const bankListWithAll = computed(() => ['전체', ...bankList.value])

// 예치기간 목록
const termList = computed(() => [6, 12, 24, 36])
const termListWithAll = computed(() => ['전체', ...termList.value])

// 상품구분 목록
const categoryList = computed(() => {
  return [...new Set(props.products.map((item) => item.category))]
})

const categoryListWithAll = computed(() => ['전체', ...categoryList.value])

const updateFilters = () => {
  emit('update:filters', {
    bank: selectedBank.value === '전체' ? null : selectedBank.value,
    term: selectedTerm.value === '전체' ? null : selectedTerm.value,
    category: selectedCategory.value === '전체' ? null : selectedCategory.value,
  })
  emit(
    'update:selectedTerm',
    selectedTerm.value === '전체' ? null : selectedTerm.value
  )
}
</script>
