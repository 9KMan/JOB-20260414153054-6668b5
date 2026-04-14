<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Subscriptions</h1>
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">ID</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">User ID</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Plan ID</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Status</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Started</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Expires</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in subscriptions" :key="sub.id" class="border-t">
            <td class="px-4 py-3">{{ sub.id }}</td>
            <td class="px-4 py-3">{{ sub.user_id }}</td>
            <td class="px-4 py-3">{{ sub.plan_id }}</td>
            <td class="px-4 py-3">
              <span :class="sub.status === 'active' ? 'text-green-600' : 'text-gray-600'" class="text-sm">
                {{ sub.status }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm">{{ formatDate(sub.started_at) }}</td>
            <td class="px-4 py-3 text-sm">{{ formatDate(sub.expires_at) }}</td>
          </tr>
          <tr v-if="!subscriptions.length">
            <td colspan="6" class="px-4 py-8 text-center text-gray-500">No subscriptions found</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../composables/useApi'

const subscriptions = ref([])

onMounted(async () => {
  try {
    const response = await api.get('/api/subscriptions')
    subscriptions.value = response.data.subscriptions
  } catch (e) {
    console.error('Failed to load subscriptions:', e)
  }
})

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}
</script>
