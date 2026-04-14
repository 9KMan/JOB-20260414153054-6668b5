<template>
  <div class="min-h-screen">
    <nav class="bg-white shadow mb-6">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 class="text-xl font-bold">SaaS Platform</h1>
        <div class="flex items-center gap-4">
          <router-link to="/dashboard" class="text-gray-600 hover:text-gray-900">Dashboard</router-link>
          <router-link v-if="isAdmin" to="/users" class="text-gray-600 hover:text-gray-900">Users</router-link>
          <router-link to="/subscription" class="text-gray-600 hover:text-gray-900 font-semibold">Subscription</router-link>
          <button @click="logout" class="text-red-600 hover:text-red-700">Logout</button>
        </div>
      </div>
    </nav>
    <div class="max-w-4xl mx-auto px-4">
      <h2 class="text-2xl font-bold mb-6">Subscription</h2>
      
      <div v-if="subscription" class="bg-white p-6 rounded shadow mb-6">
        <h3 class="text-lg font-semibold mb-4">Current Plan</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500">Plan</p>
            <p class="font-medium">{{ plan?.name }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Status</p>
            <p class="font-medium capitalize">{{ subscription.status }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Billing Cycle</p>
            <p class="font-medium capitalize">{{ subscription.billing_cycle }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Renews</p>
            <p class="font-medium">{{ formatDate(subscription.current_period_end) }}</p>
          </div>
        </div>
        <button v-if="subscription.status !== 'canceled'" @click="cancelSubscription" 
          class="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
          Cancel Subscription
        </button>
      </div>
      
      <div v-if="!subscription">
        <h3 class="text-lg font-semibold mb-4">Available Plans</h3>
        <div v-if="loadingPlans" class="text-gray-500">Loading plans...</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div v-for="p in plans" :key="p.id" class="bg-white p-4 rounded shadow border-2 border-transparent hover:border-blue-500">
            <h4 class="font-semibold text-lg mb-2">{{ p.name }}</h4>
            <p class="text-2xl font-bold mb-1">${{ p.price_monthly }}<span class="text-sm text-gray-500">/mo</span></p>
            <ul class="text-sm text-gray-600 mb-4">
              <li v-for="(val, key) in p.features" :key="key" class="py-1">{{ key }}: {{ val }}</li>
            </ul>
            <button @click="subscribe(p.id)" :disabled="subscribing"
              class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50">
              Subscribe
            </button>
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
const { get, post } = useApi()
const subscription = ref(null)
const plan = ref(null)
const plans = ref([])
const isAdmin = ref(false)
const loadingPlans = ref(false)
const subscribing = ref(false)

onMounted(async () => {
  const user = JSON.parse(localStorage.getItem("user") || "{}")
  isAdmin.value = user.role === "admin"
  await fetchSubscription()
  await fetchPlans()
})

async function fetchSubscription() {
  try {
    const { data } = await get("/subscriptions/")
    subscription.value = data.subscription
    plan.value = data.plan
  } catch (err) { console.error(err) }
}

async function fetchPlans() {
  loadingPlans.value = true
  try {
    const { data } = await get("/subscriptions/plans")
    plans.value = data.plans
  } catch (err) { console.error(err) }
  finally { loadingPlans.value = false }
}

async function subscribe(planId) {
  subscribing.value = true
  try {
    const { data } = await post("/subscriptions/", { plan_id: planId, billing_cycle: "monthly" })
    subscription.value = data.subscription
    await fetchSubscription()
  } catch (err) { alert(err.response?.data?.error || "Subscription failed") }
  finally { subscribing.value = false }
}

async function cancelSubscription() {
  if (!confirm("Cancel this subscription?")) return
  try {
    const { data } = await post(`/subscriptions/${subscription.value.id}/cancel`)
    subscription.value = data.subscription
  } catch (err) { alert("Failed to cancel") }
}

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
