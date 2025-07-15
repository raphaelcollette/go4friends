import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useFriendStore = defineStore('friend', {
  state: () => ({
    friends: [],
    pendingRequests: [],
    suggested: [],
    searchResults: [],
    loading: false,
    lastFetched: null, // for caching
    suggestionsLastFetched: null,
    friendCountCache: {},
  }),

  actions: {
    async fetchFriends(force = false) {
      const oneMinute = 60 * 1000
      if (!force && this.lastFetched && Date.now() - this.lastFetched < oneMinute) {
        return
      }

      this.loading = true
      try {
        const res = await authAxios.get('/friends/friends/')
        this.friends = res.data

        const pending = await authAxios.get('/friends/requests/')
        this.pendingRequests = pending.data

        this.lastFetched = Date.now() // 🕒 update last fetch time
      } catch (error) {
        console.error('Failed to fetch friends:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchSuggestions(force = false) {
        const oneMinute = 60 * 1000
        if (!force && this.suggestionsLastFetched && Date.now() - this.suggestionsLastFetched < oneMinute) {
          return
        }
      
        try {
          const res = await authAxios.get('/friends/suggestions/')
          this.suggested = res.data
          this.suggestionsLastFetched = Date.now()
        } catch (error) {
          console.error('Failed to fetch suggestions:', error)
        }
      },

    async acceptRequest(username) {
      try {
        await authAxios.post('/friends/accept/', { from_username: username })
        await this.fetchFriends(true) // ✅ force refresh
      } catch (error) {
        console.error('Failed to accept request:', error)
        throw error
      }
    },

    async rejectRequest(username) {
      try {
        await authAxios.post('/friends/reject/', { from_username: username })
        await this.fetchFriends(true)
      } catch (error) {
        console.error('Failed to reject request:', error)
        throw error
      }
    },

    async removeFriend(username) {
      try {
        await authAxios.post('/friends/remove/', { username })
        await this.fetchFriends(true)
      } catch (error) {
        console.error('Failed to remove friend:', error)
        throw error
      }
    },

    async searchUsers(query) {
      if (!query.trim()) {
        this.searchResults = []
        return
      }

      try {
        const res = await authAxios.get(`/users/search/?q=${encodeURIComponent(query)}`)
        this.searchResults = res.data
      } catch (error) {
        console.error('User search failed:', error)
        throw error
      }
    },

    async fetchFriendCount(username, force = false) {
      const oneMinute = 60 * 1000
      const cached = this.friendCountCache[username]

      if (!force && cached && (Date.now() - cached.fetchedAt) < oneMinute) {
        return cached.count
      }

      try {
        const res = await authAxios.get(`/friends/${encodeURIComponent(username)}/count/`)
        this.friendCountCache[username] = {
          count: res.data.friends_count,
          fetchedAt: Date.now(),
        }
        return res.data.friends_count
      } catch (error) {
        console.error('Failed to fetch friend count:', error)
        this.friendCountCache[username] = {
          count: null,
          fetchedAt: Date.now(),
        }
        return null
      }
    },

    reset() {
        this.friends = []
        this.pendingRequests = []
        this.suggested = []
        this.searchResults = []
        this.loading = false
        this.lastFetched = null
        this.suggestionsLastFetched = null
      }
  }
})
