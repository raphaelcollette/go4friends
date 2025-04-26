import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useEventStore = defineStore('event', {
  state: () => ({
    events: [],
    lastFetched: null,
    loading: false,
  }),

  getters: {
    filteredEvents: (state) => (type = '') => {
      if (!type) return state.events
      return state.events.filter(event =>
        type === 'club' ? event.club : !event.club
      )
    },
    sortedEvents: (state) => (events, sortOrder = 'date') => {
      return [...events].sort((a, b) => {
        if (sortOrder === 'date') return new Date(a.date) - new Date(b.date)
        return a.title.localeCompare(b.title)
      })
    }
  },

  actions: {
    async fetchEvents(force = false) {
      const cacheTime = 30 * 1000; // 30 seconds
      const now = Date.now();
    
      if (!force && this.lastFetched && (now - this.lastFetched < cacheTime)) {
        return; // ✅ Use cache if recent and not forcing
      }
    
      this.loading = true;
      try {
        const res = await authAxios.get('/events/', { params: { upcoming: true } });
        if (Array.isArray(res.data)) {
          this.events = res.data; // ✅ Always update events array
        } else {
          console.error('Unexpected events response format:', res.data);
          this.events = [];
        }
        this.lastFetched = now;
      } catch (error) {
        console.error('Failed to fetch events:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createEvent(formData) {
      await authAxios.post('/events/create/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      await this.fetchEvents(true)
    },

    async rsvp(eventId) {
      await authAxios.post(`/events/${eventId}/rsvp/`)
      await this.fetchEvents(true)
    },

    async cancelRsvp(eventId) {
      await authAxios.post(`/events/${eventId}/cancel-rsvp/`)
      await this.fetchEvents(true)
    },

    async deleteEvent(id) {
      await authAxios.delete(`/events/${id}/delete/`)
      this.events = this.events.filter(event => event.id !== id)
    },

    async updateEvent(eventId, formData) {
      await authAxios.put(`/events/${eventId}/update/`, formData)
    },

    reset() {
      this.events = []
      this.lastFetched = null
      this.loading = false
    }
  }
})

