import { createRouter, createWebHistory } from 'vue-router'
import Signup from '@/pages/Signup.vue'
import Login from '@/pages/Login.vue'
import Profile from '@/pages/Profile.vue'
import Home from '@/pages/Home.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
