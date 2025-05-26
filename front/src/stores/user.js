// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    username: '',
    isAuthenticated: false,
  }),
  actions: {
    setUser({ token, username }) {
      this.token = token
      this.username = username
      this.isAuthenticated = true
    },
    logout() {
      this.token = null
      this.username = ''
      this.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
})
