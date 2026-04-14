<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md p-8 bg-white rounded-lg shadow">
      <h1 class="text-2xl font-bold mb-6 text-center">Sign In</h1>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Email</label>
          <input v-model="form.email" type="email" required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium mb-1">Password</label>
          <input v-model="form.password" type="password" required
            class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div v-if="error" class="mb-4 text-red-600 text-sm">{{ error }}</div>
        <button type="submit" :disabled="loading"
          class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50">
          {{ loading ? "Signing in..." : "Sign In" }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm">
        Don't have an account? <router-link to="/register" class="text-blue-600">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useApi } from "../composables/useApi"

const router = useRouter()
const { post } = useApi()
const form = ref({ email: "", password: "" })
const error = ref("")
const loading = ref(false)

async function login() {
  loading.value = true
  error.value = ""
  try {
    const { data } = await post("/auth/login", form.value)
    localStorage.setItem("access_token", data.access_token)
    localStorage.setItem("refresh_token", data.refresh_token)
    localStorage.setItem("user", JSON.stringify(data.user))
    router.push("/dashboard")
  } catch (err) {
    error.value = err.response?.data?.error || "Login failed"
  } finally {
    loading.value = false
  }
}
</script>
