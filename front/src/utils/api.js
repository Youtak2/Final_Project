// src/utils/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',  // Django API 기본 URL
  timeout: 10000,
})

// 필요하면 요청 인터셉터에서 토큰 자동 추가 설정 가능
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`  // 'Bearer' → 'Token' 으로 변경
  }
  return config
}, error => Promise.reject(error))


export default api
