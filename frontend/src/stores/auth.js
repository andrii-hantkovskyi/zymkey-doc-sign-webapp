import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const isAuthenticated = ref(!!token.value)
  const username = ref(localStorage.getItem('username') || '')
  const isAdmin = ref(localStorage.getItem('isAdmin') === 'true')

  const setToken = (value) => {
    token.value = value
    localStorage.setItem('token', value)
    isAuthenticated.value = !!value
  }

  const setUsername = (value) => {
    username.value = value
    localStorage.setItem('username', value)
  }

  const setIsAdmin = (value) => {
    isAdmin.value = value
    localStorage.setItem('isAdmin', value.toString())
  }

  const logout = () => {
    token.value = ''
    isAuthenticated.value = false
    username.value = ''
    isAdmin.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('isAdmin')
  }

  return {
    token,
    isAuthenticated,
    username,
    isAdmin,
    setToken,
    setUsername,
    setIsAdmin,
    logout,
  }
})
