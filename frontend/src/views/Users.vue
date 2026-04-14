<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Users</h1>
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">ID</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Name</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Email</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Status</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Joined</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-t">
            <td class="px-4 py-3">{{ user.id }}</td>
            <td class="px-4 py-3">{{ user.full_name || '-' }}</td>
            <td class="px-4 py-3">{{ user.email }}</td>
            <td class="px-4 py-3">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'" class="text-sm">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(user.created_at) }}</td>
          </tr>
          <tr v-if="!users.length">
            <td colspan="5" class="px-4 py-8 text-center text-gray-500">No users found</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="mt-4 flex justify-center">
      <button @click="loadUsers" :disabled="loading" class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
        {{ loading ? 'Loading...' : 'Load More' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../composables/useApi'

const users = ref([])
const loading = ref(false)
const page = ref(1)

onMounted(() => loadUsers())

async function loadUsers() {
  loading.value = true
  try {
    const response = await api.get(`/api/users?page=${page.value}&per_page=20`)
    users.value = response.data.users
  } catch (e) {
    console.error('Failed to load users:', e)
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString()
}
</script>
