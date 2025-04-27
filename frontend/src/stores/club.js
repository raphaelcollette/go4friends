import { defineStore } from 'pinia'
import { authAxios } from '@/utils/axios'

export const useClubStore = defineStore('club', {
  state: () => ({
    clubs: [],
    myClubs: [],
    lastFetched: null,
    myClubsLastFetched: false,
    currentClub: null,
    clubMembers: [],
    loadingClub: false,
    suggestedClubs: [],
    suggestedLastFetched: null,
  }),
  actions: {
    async fetchClubs(force = false) {
      const oneMinute = 60 * 1000
      if (!force && this.lastFetched && Date.now() - this.lastFetched < oneMinute) return
      const res = await authAxios.get('/clubs/')
      this.clubs = res.data
      this.lastFetched = Date.now()
    },

    async createClub({ name, description, is_private = false }) {
      await authAxios.post('/clubs/create/', { name, description, is_private })
      await this.fetchClubs(true)
    },

    async fetchClubProfile(clubName) {
      this.loadingClub = true
      try {
        const existingClub = this.clubs.find(c => c.name === clubName)

        if (existingClub) {
          this.currentClub = existingClub
        } else {
          const res = await authAxios.get('/clubs/')
          this.clubs = res.data
          this.currentClub = this.clubs.find(c => c.name === clubName) || null
        }

        const memberRes = await authAxios.get(`/clubs/${encodeURIComponent(clubName)}/profile/`)
        this.clubMembers = memberRes.data.members
      } catch (error) {
        console.error('Failed to fetch club profile:', error)
        this.currentClub = null
        this.clubMembers = []
        throw error
      } finally {
        this.loadingClub = false
      }
    },

    async joinClub(name) {
      await authAxios.post(`/clubs/${encodeURIComponent(name)}/join/`)
      await this.fetchClubs(true)
    },

    async leaveClub(name) {
      await authAxios.post(`/clubs/${encodeURIComponent(name)}/leave/`)
      await this.fetchClubs(true)
    },

    async fetchMyClubs(force = false) {
      const now = Date.now()
      const oneMinute = 60 * 1000
    
      if (!force && this.myClubsLastFetched && (now - this.myClubsLastFetched < oneMinute)) {
        return // 
      }
    
      try {
        const res = await authAxios.get('/clubs/my/')
        this.myClubs = res.data
        this.myClubsLastFetched = now // 
      } catch (error) {
        console.error('Failed to fetch my clubs:', error)
        this.myClubs = []
        this.myClubsLastFetched = null
      }
    },


    async fetchSuggestedClubs(force = false) {
      const now = Date.now()
      const oneMinute = 60 * 1000

      if (!force && this.suggestedLastFetched && (now - this.suggestedLastFetched < oneMinute)) {
        return 
      }

      try {
        const res = await authAxios.get('/clubs/suggested/')
        this.suggestedClubs = res.data
        this.suggestedLastFetched = now
      } catch (error) {
        console.error('Error fetching suggested clubs:', error)
      }
    },

    reset() {
      this.clubs = []
      this.myClubs = []
      this.myClubsFetched = false
      this.lastFetched = null
      this.currentClub = null
      this.clubMembers = []
      this.loadingClub = false
    }
  },
  persist: {
    paths: ['clubs'],
    storage: localStorage,
  }
})
