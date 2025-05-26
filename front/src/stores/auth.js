import { ref, computed, watch } from "vue"
import { defineStore } from "pinia"
import axios from "axios"

export const useAuthStore = defineStore("auth", () => {
  // 상태
  const token = ref(localStorage.getItem("token") || null)
  const user = ref(null)

  // 계산된 상태
  const isLogin = computed(() => !!token.value)

  // axios 헤더 설정
  function applyTokenToAxios(tokenValue) {
    if (tokenValue) {
      axios.defaults.headers.common["Authorization"] = `Token ${tokenValue}`
    } else {
      delete axios.defaults.headers.common["Authorization"]
    }
  }

  // 토큰 저장
  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem("token", newToken)
    applyTokenToAxios(newToken)
  }

  // 사용자 정보 불러오기
  async function fetchUser() {
    if (!token.value) return
    try {
      applyTokenToAxios(token.value)
      const res = await axios.get("http://localhost:8000/api/v1/accounts/user/")
      user.value = res.data
    } catch (error) {
      console.error("❌ 사용자 정보 가져오기 실패", error)
    }
  }

  // 로그아웃
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem("token")
    applyTokenToAxios(null)
  }

  // localStorage 변화 감지
  window.addEventListener("storage", (event) => {
    if (event.key === "token") {
      token.value = event.newValue
      applyTokenToAxios(event.newValue)
    }
  })

  // 토큰 변화 감지해 동기화
  watch(token, (newVal) => {
    if (!newVal) {
      localStorage.removeItem("token")
      user.value = null
    } else {
      localStorage.setItem("token", newVal)
      applyTokenToAxios(newVal)
    }
  })

  return {
    token,
    user,
    isLogin,
    setToken,
    fetchUser,
    logout,
  }
})
