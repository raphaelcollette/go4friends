import { createRouter, createWebHistory } from 'vue-router'
import Signup from '@/pages/Signup.vue'
import Login from '@/pages/Login.vue'
import Main from '@/pages/Main.vue'
import Home from '@/pages/Home.vue'
import Profile from '@/pages/Profile.vue'
import Friends from '@/pages/Friends.vue'
import EditProfile from '@/pages/EditProfile.vue'
import UserProfile from '@/pages/UserProfile.vue'
import Settings from '@/pages/Settings.vue'
import Events from '@/pages/Events.vue'
import Clubs from '@/pages/Clubs.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: (to, from, next) => {
      const isLoggedIn = !!localStorage.getItem('access_token')
      if (isLoggedIn) {
        next('/main')
      } else {
        next()
      }
    }
  },
  { path: '/signup', component: Signup },
  { path: '/login', component: Login },
  { 
    path: '/main',
    name: 'Main',
    component: Main,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  { 
    path: '/friends',
    name: 'Friends',
    component: Friends,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/edit',
    name: 'EditProfile',
    component: EditProfile,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/:username',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  { 
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  },
  { path: '/events', name: 'Events', component: Events, meta: { requiresAuth: true } },
  { path: '/clubs', name: 'Clubs', component: Clubs, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Global auth guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login') // If trying to access a protected page without login
  } else {
    next()
  }
})

export default router
