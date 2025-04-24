import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useInviteStore = defineStore('invite', {
  state: () => ({
    invites: [],
    lastFetched: null, // ⏱ timestamp
  }),
  actions: {
    async fetchInvites(force = false) {
      const oneMinute = 60 * 1000
      if (!force && this.lastFetched && Date.now() - this.lastFetched < oneMinute) {
        return // ⛔ skip re-fetching if cached recently
      }

      try {
        const res = await authAxios.get('/clubs/invites/')
        this.invites = res.data
        this.lastFetched = Date.now()
      } catch (err) {
        console.error('Failed to fetch invites:', err)
        this.invites = []
      }
    },

    async acceptInvite(inviteId) {
      await authAxios.post(`/clubs/invites/${inviteId}/accept/`)
      await this.fetchInvites(true) // ✅ force refresh
    },

    async rejectInvite(inviteId) {
      await authAxios.post(`/clubs/invites/${inviteId}/reject/`)
      await this.fetchInvites(true) // ✅ force refresh
    },
  },
})