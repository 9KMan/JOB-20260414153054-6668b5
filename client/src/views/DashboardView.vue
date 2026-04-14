<template>
  <div class="min-h-screen">
    <nav class="bg-white shadow mb-6">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold">SaaS Platform</h1>
        <div class="flex items-center gap-4">
          <router-link to="/dashboard" class="text-gray-600 hover:text-gray-900">Dashboard</router-link>
          <router-link v-if="isAdmin" to="/users" class="text-gray-600 hover:text-gray-900">Users</router-link>
          <router-link to="/subscription" class="text-gray-600 hover:text-gray-900">Subscription</router-link>
          <button @click="logout" class="text-red-600 hover:text-red-700">Logout</button>
        </div>
      </div>
    </nav>
    <div class="max-w-7xl mx-auto px-4">
      <h2 class="text-2xl font-bold mb-6">Dashboard</h2>
      <div v-if="loading" class="text-gray-500">Loading...</div>
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-4 rounded shadow">
            <p class="text-sm text-gray-500">Total Users</p>
            <p class="text-2xl font-bold">{{ stats.total_users }}</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-sm text-gray-500">Active Users</p>
            <p class="text-2xl font-bold">{{ stats.active_users }}</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-sm text-gray-500">Total Subscriptions</p>
            <p class="text-2xl font-bold">{{ stats.total_subscriptions }}</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-sm text-gray-500">Active Subscriptions</p>
            <p class="text-2xl font-bold">{{ stats.active_subscriptions }}</p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white p-4 rounded shadow">
            <h3 class="font-semibold mb-4">Recent Signups</h3>
            <div v-for="user in recentSignups" :key="user.id" class="py-2 border-b last:border-0">
              <p class="font-medium">{{ user.full_name }}</p>
              <p class="text-sm text-gray-500">{{ user.email }}</p>
            </div>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <h3 class="font-semibold mb-4">Recent Activity</h3>
            <div v-for="activity in recentActivity" :key="activity.created_at" class="py-2 border-b last:border-0">
              <p class="text-sm font-medium">{{ activity.action }}</p>
              <p class="text-xs text-gray-500">{{ activity.resource }} &middot; {{ formatDate(activity.created_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useApi } from "../composables/useApi"

const router = useRouter()
const { get } = useApi()
const stats = ref({ total_users: 0, active_users: 0, total_subscriptions: 0, active_subscriptions: 0 })
const recentSignups = ref([])
const recentActivity = ref([])
const isAdmin = ref(false)
const loading = ref(true)

onMounted(async () => {
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}")
    isAdmin.value = user.role === "admin"
    const { data } = await get("/dashboard/stats")
    stats.value = data.stats
    recentSignups.value = data.recent_signups
    recentActivity.value = data.recent_activity
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

function formatDate(iso) {
  if (!iso) return ""
  return new Date(iso).toLocaleString()
}

function logout() {
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
  localStorage.removeItem("user")
  router.push("/login")
}
</script>
