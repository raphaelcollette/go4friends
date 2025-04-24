import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useInviteStore = defineStore('invite', {
  state: () => ({
    invites: [],
  }),
  actions: {
    async fetchInvites() {
      const res = await authAxios.get('/clubs/invites/')
      this.invites = res.data
    },

    async acceptInvite(inviteId) {
      await authAxios.post(`/clubs/invites/${inviteId}/accept/`)
      await this.fetchInvites()
    },

    async rejectInvite(inviteId) {
      await authAxios.post(`/clubs/invites/${inviteId}/reject/`)
      await this.fetchInvites()
    },
  },
})