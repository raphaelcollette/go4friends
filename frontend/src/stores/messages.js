import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useMessageStore = defineStore('messages', {
  state: () => ({
    threads: [],
    lastFetched: null,
    messagesByThread: {},
    loadingByThread: {},
    pinnedMessages: {},
  }),

  actions: {
    async fetchThreads(force = false) {
      const now = Date.now()
      const fiveMinutes = 5 * 60 * 1000

      if (!force && this.lastFetched && now - this.lastFetched < fiveMinutes) return

      try {
        const res = await authAxios.get('/messages/threads/')
        this.threads = res.data
        this.lastFetched = now
      } catch (error) {
        console.error('Failed to fetch threads:', error)
        throw error
      }
    },

    async fetchMessages(threadId, force = false) {
        if (!force && this.messagesByThread[threadId]) {
          return // already cached
        }
      
        if (this.loadingByThread[threadId]) return
        this.loadingByThread[threadId] = true
      
        try {
          const res = await authAxios.get(`/messages/threads/${threadId}/messages/`)
          this.messagesByThread[threadId] = res.data
        } catch (error) {
          console.error(`Failed to fetch messages for thread ${threadId}:`, error)
          throw error
        } finally {
          this.loadingByThread[threadId] = false
        }
      },

      async sendMessage(threadId, message) {
        try {
          await authAxios.post(`/messages/threads/${threadId}/send/`, { message })
          await this.fetchMessages(threadId, true) // ✅ force reload
        } catch (error) {
          console.error('Failed to send message:', error)
          throw error
        }
      },

    async startGroupThread(usernames) {
      const res = await authAxios.post('/messages/threads/start-private/', { usernames })
      await this.fetchThreads(true)
      return res.data
    },

    async fetchPinnedMessages(threadId) {
      try {
        // Reuse full message list if already fetched
        const all = this.messagesByThread[threadId]
        if (all) {
          this.pinnedMessages[threadId] = all.filter(msg => msg.pinned)
        } else {
          // Otherwise fetch and filter
          const res = await authAxios.get(`/messages/threads/${threadId}/messages/`)
          this.pinnedMessages[threadId] = res.data.filter(msg => msg.pinned)
        }
      } catch (error) {
        console.error(`Failed to fetch pinned messages for thread ${threadId}:`, error)
        this.pinnedMessages[threadId] = []
      }
    },

    async togglePin(messageId, threadId) {
      try {
        await authAxios.post(`messages/messages/${messageId}/pin/`)
        await this.fetchPinnedMessages(threadId)
      } catch (error) {
        console.error(`Failed to toggle pin for message ${messageId}:`, error)
        throw error
      }
    },


    reset() {
      this.threads = []
      this.lastFetched = null
      this.messagesByThread = {}
      this.loadingByThread = {}
    }
  }
})
