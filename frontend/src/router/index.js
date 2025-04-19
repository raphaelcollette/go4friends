import { createRouter, createWebHistory } from 'vue-router'
import Signup from '@/pages/Signup.vue'
import Login from '@/pages/Login.vue'
import Profile from '@/pages/Profile.vue'

const routes = [
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile },
  { path: '/', redirect: '/login' }, // default route
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
