import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../composables/useApi'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  
  const isAuthenticated = computed(() => !!token.value)
  
  async function login(email, password) {
    const response = await api.post('/api/auth/login', { email, password })
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('token', token.value)
    return response.data
  }
  
  async function register(data) {
    const response = await api.post('/api/auth/register', data)
    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('token', token.value)
    return response.data
  }
  
  async function fetchUser() {
    if (!token.value) return null
    try {
      const response = await api.get('/api/auth/me')
      user.value = response.data.user
      return user.value
    } catch (e) {
      logout()
      return null
    }
  }
  
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }
  
  return { user, token, isAuthenticated, login, register, fetchUser, logout }
})
