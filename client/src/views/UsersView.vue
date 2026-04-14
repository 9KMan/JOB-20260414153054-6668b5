<template>
  <div class="min-h-screen">
    <nav class="bg-white shadow mb-6">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold">SaaS Platform</h1>
        <div class="flex items-center gap-4">
          <router-link to="/dashboard" class="text-gray-600 hover:text-gray-900">Dashboard</router-link>
          <router-link to="/users" class="text-gray-600 hover:text-gray-900 font-semibold">Users</router-link>
          <router-link to="/subscription" class="text-gray-600 hover:text-gray-900">Subscription</router-link>
          <button @click="logout" class="text-red-600 hover:text-red-700">Logout</button>
        </div>
      </div>
    </nav>
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Users</h2>
        <input v-model="search" @input="debouncedSearch" placeholder="Search users..."
          class="px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div class="bg-white rounded shadow overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Name</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Email</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Role</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Status</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">Joined</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="user in users" :key="user.id">
              <td class="px-4 py-3">{{ user.full_name }}</td>
              <td class="px-4 py-3">{{ user.email }}</td>
              <td class="px-4 py-3">
                <span :class="user.role === 'admin' ? 'text-purple-600' : 'text-gray-600'" class="text-sm">{{ user.role }}</span>
              </td>
              <td class="px-4 py-3">
                <span :class="user.is_active ? 'text-green-600' : 'text-red-600'" class="text-sm">{{ user.is_active ? "Active" : "Inactive" }}</span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(user.created_at) }}</td>
            </tr>
          </tbody>
        </table>
        <div class="p-4 flex justify-between items-center">
          <p class="text-sm text-gray-500">Total: {{ total }} users</p>
          <div class="flex gap-2">
            <button @click="prevPage" :disabled="page <= 1" class="px-3 py-1 border rounded disabled:opacity-50">Prev</button>
            <button @click="nextPage" :disabled="page >= pages" class="px-3 py-1 border rounded disabled:opacity-50">Next</button>
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
const users = ref([])
const search = ref("")
const page = ref(1)
const total = ref(0)
const pages = ref(1)
const loading = ref(false)

onMounted(() => fetchUsers())

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await get("/users", { page: page.value, search: search.value })
    users.value = data.users
    total.value = data.total
    pages.value = data.pages
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function debouncedSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; fetchUsers() }, 400)
}
let debounceTimer

function prevPage() { if (page.value > 1) { page.value--; fetchUsers() } }
function nextPage() { if (page.value < pages.value) { page.value++; fetchUsers() } }

function formatDate(iso) {
  if (!iso) return ""
  return new Date(iso).toLocaleDateString()
}

function logout() {
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
  localStorage.removeItem("user")
  router.push("/login")
}
</script>
