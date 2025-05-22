import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const BACKEND_SERVER_URL = import.meta.env.VITE_BACKEND_SERVER_URL
  const token = ref(null)
  const username = ref(null)
  const router = useRouter()
  const userInfo = ref(null)
  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const getUserInfo = async (userId) => {
    try {
      const res = await axios.get(`${BACKEND_SERVER_URL}/user/detail/${userId}/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      console.log('User Info:', res.data)
      userInfo.value = res.data
    } catch (err) {
      console.error('Failed to get user info:', err)
    }
  }

  const signUp = async (payload) => {
    try {
      const response = await axios({
      method: 'post',
      url: `${BACKEND_SERVER_URL}/accounts/signup/`,
      data: payload,
    })
    
    if (response.data.key) {
      token.value = response.data.key
      username.value = payload.username
      router.push({ name: 'ArticleView' })
    }
  } catch (error) {
    console.error(error)
    throw error
  }
}

  const signOut = async function (userId) {
    try {
      await axios({
        method: 'delete',
        url: `${BACKEND_SERVER_URL}/user/detail/${userId}/`,
        headers: {
          Authorization: `Token ${token.value}`,
        }
      })
      token.value = null
      userInfo.value = null
      router.push({ name: 'ArticleView'})
    } catch (error) {
      console.error('회원탈퇴 실패:', error)
    }
  }

    const logIn = async (payload) => {
      try {
        const response = await axios({
          method: 'post',
          url: `${BACKEND_SERVER_URL}/accounts/login/`,
          data: payload,
        })
        token.value = response.data.key
        username.value = payload.username
        router.go(-1)
      } catch (error) {
        console.error('로그인 실패:', error)
        alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.')
      }
    }

    const logOut = async () => {
      try {
        await axios({
          method: 'post',
          url: `${BACKEND_SERVER_URL}/accounts/logout/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        })
        token.value = null
        username.value = null
        router.push({ name: 'HomeView'})
      } catch (error) {
        console.error('로그아웃 실패:', error)
      }
    }

  return { 
    token,
    username,
    isLogin,
    BACKEND_SERVER_URL,
    userInfo,
    signUp,
    signOut,
    logIn,
    logOut,
    getUserInfo,
  }
}, {persist:true}
)
