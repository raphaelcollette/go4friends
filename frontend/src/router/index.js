import { createRouter, createWebHistory } from 'vue-router'
import Signup from '@/pages/Signup.vue'
import Login from '@/pages/Login.vue'
import Main from '@/pages/Main.vue'
import Home from '@/pages/Home.vue'
import Profile from '@/pages/Profile.vue'
import Friends from '@/pages/Friends.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { path: '/main',
    name: 'Main',
    component: Main,
    meta: { requiresAuth: true }
   },
  { path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
   },
   { path: '/friends',
     name: 'Friends',
     component: Friends,
     meta: { requiresAuth: true}
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !isLoggedIn) {
    // If trying to go to a protected page and not logged in ➔ Redirect to Login
    next('/login')
  } else {
    // Otherwise, continue normally
    next()
  }
})

export default router
