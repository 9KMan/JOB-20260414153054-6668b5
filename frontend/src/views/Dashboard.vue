<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Dashboard</h1>
      <button @click="handleLogout" class="bg-red-500 text-white px-4 py-2 rounded">Logout</button>
    </div>
    
    <div v-if="loading" class="text-center py-8">Loading...</div>
    <div v-else-if="stats" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Total Users</h3>
        <p class="text-3xl font-bold">{{ stats.total_users }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Active Users</h3>
        <p class="text-3xl font-bold">{{ stats.active_users }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Active Subscriptions</h3>
        <p class="text-3xl font-bold">{{ stats.active_subscriptions }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-gray-500 text-sm">Plans</h3>
        <p class="text-3xl font-bold">{{ stats.total_plans }}</p>
      </div>
    </div>
    
    <div class="bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-bold mb-4">Recent Signups</h2>
      <table class="w-full">
        <thead>
          <tr class="text-left border-b">
            <th class="pb-2">Name</th>
            <th class="pb-2">Email</th>
            <th class="pb-2">Joined</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in recentSignups" :key="user.id" class="border-b last:border-0">
            <td class="py-3">{{ user.full_name }}</td>
            <td class="py-3">{{ user.email }}</td>
            <td class="py-3">{{ formatDate(user.created_at) }}</td>
          </tr>
          <tr v-if="!recentSignups?.length">
            <td colspan="3" class="py-4 text-gray-500 text-center">No recent signups</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../composables/useApi'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref(null)
const recentSignups = ref([])
const loading = ref(true)

onMounted(async () => {
  await authStore.fetchUser()
  await loadStats()
  loading.value = false
})

async function loadStats() {
  try {
    const response = await api.get('/api/dashboard/stats')
    stats.value = response.data.stats
    recentSignups.value = response.data.recent_signups
  } catch (e) {
    console.error('Failed to load stats:', e)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
