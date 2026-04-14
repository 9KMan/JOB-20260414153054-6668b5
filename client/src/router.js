import { createRouter, createWebHistory } from "vue-router"

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/login", component: () => import("./views/LoginView.vue") },
  { path: "/register", component: () => import("./views/RegisterView.vue") },
  { path: "/dashboard", component: () => import("./views/DashboardView.vue") },
  { path: "/users", component: () => import("./views/UsersView.vue") },
  { path: "/subscription", component: () => import("./views/SubscriptionView.vue") },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token")
  if (!token && to.path !== "/login" && to.path !== "/register") {
    next("/login")
  } else {
    next()
  }
})

export default router
