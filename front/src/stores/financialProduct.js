import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'

export const useFinanceStore = defineStore(
  'Finance',
  () => {
    const authStore = useAuthStore()

    const recommendProducts = ref(null)
    const financialProducts = ref([])
    const selectedProduct = ref(null)
    const BACKEND_SERVER_URL = import.meta.env.VITE_BACKEND_SERVER_URL

    const getFinancialProducts = async () => {
      try {
        const response = await axios({
          method: 'get',
          url: `${BACKEND_SERVER_URL}/finances/infos/`,
        })
        console.log('상품 정보 조회 성공:', response)
        financialProducts.value = response.data.prdt_data
      } catch (error) {
        console.error('상품 정보 조회 실패:', error)
      }
    }

    const getProductDetailFromServer = async (productUniqueId) => {
      try {
        const response = await axios({
          method: 'get',
          url: `${BACKEND_SERVER_URL}/finances/infos/${productUniqueId}/`,
          headers: {
            Authorization: `Token ${authStore.token}`,
          },
        })
        console.log('상품 상세 정보 조회 성공:', response)
        selectedProduct.value = response.data
      } catch (error) {
        console.error('상품 상세 정보 조회 실패:', error)
      }
    }

    const setRecommendProducts = (data) => {
      recommendProducts.value = data
      console.log(recommendProducts.value)
    }

    return {
      financialProducts,
      selectedProduct,
      recommendProducts,
      getFinancialProducts,
      getProductDetailFromServer,
      setRecommendProducts
    }
  },
  { persist: true }
)
