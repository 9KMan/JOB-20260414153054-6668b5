<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold mb-6 text-center">Sign In</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input v-model="email" type="email" required 
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md" />
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700">Password</label>
          <input v-model="password" type="password" required 
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
        <p v-if="error" class="mt-4 text-red-600 text-sm">{{ error }}</p>
      </form>
      <p class="mt-4 text-center text-sm">
        Don't have an account? <router-link to="/register" class="text-blue-600">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
