import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()  // ✅ Pinia 상태 사용
  const token = auth.token || localStorage.getItem('token')  // ✅ 둘 다 fallback
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
}, (error) => Promise.reject(error))

export default api
