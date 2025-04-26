import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: JSON.parse(localStorage.getItem('currentUser')) || null, // ✅ load immediately
    notifications: [],
    unreadCount: 0,
    lastFetched: null,
  }),
  actions: {
    async fetchCurrentUser() {
      if (!this.currentUser) {
        const res = await authAxios.get('/users/me/')
        this.currentUser = res.data
        localStorage.setItem('currentUser', JSON.stringify(res.data)) // ✅ save it
      }
    },
    async fetchNotifications(force = false) {
        const oneMinute = 60 * 1000
      
        if (!force && this.lastFetched && Date.now() - this.lastFetched < oneMinute) {
          return
        }
      
        const res = await authAxios.get('/notifications/')
        this.notifications = res.data
        this.unreadCount = res.data.filter(n => !n.is_read).length
        this.lastFetched = Date.now()
    },
    async markAllRead() {
      await authAxios.post('/notifications/mark-read/')
      this.notifications.forEach(n => n.is_read = true)
      this.unreadCount = 0
    },
    async clearNotifications() {
      await authAxios.post('/notifications/clear/')
      this.notifications = []
      this.unreadCount = 0
    },

    reset() {
        this.currentUser = null
        this.notifications = []
        this.unreadCount = 0
        this.lastFetched = null
      }
  }
})