<template>
    <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
      <main class="flex-1 flex flex-col items-center pt-24 px-6">
        <div class="w-full max-w-6xl flex justify-between items-center mb-10">
          <h1 class="text-4xl font-extrabold text-gray-800">Clubs</h1>
          <button class="btn" @click="showCreate = true">+ Create Club</button>
        </div>
  
        <!-- Create Club Modal -->
        <div v-if="showCreate" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div class="bg-white rounded-2xl p-8 w-full max-w-md space-y-6">
            <h2 class="text-2xl font-bold text-center">Create a New Club</h2>
  
            <input v-model="newClubName" type="text" placeholder="Club Name" class="input w-full" />
            <textarea v-model="newClubDescription" placeholder="Club Description" class="input w-full"></textarea>
  
            <div class="flex justify-end space-x-4 mt-4">
              <button class="btn bg-gray-400 hover:bg-gray-500" @click="resetCreateModal">Cancel</button>
              <button class="btn bg-green-500 hover:bg-green-600" @click="createClub">Create</button>
            </div>
          </div>
        </div>
  
        <!-- Clubs List -->
        <div v-if="clubs.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl">
          <div
            v-for="club in clubs"
            :key="club.id"
            @click="club.name && goToClub(club.name)"
            class="bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <h3 class="text-2xl font-bold text-gray-800">{{ club.name }}</h3>
            <p class="text-gray-600 mt-2">{{ club.description || 'No description provided.' }}</p>
  
            <div class="mt-4">
              <button
                v-if="!club.is_member"
                class="btn bg-green-500 hover:bg-green-600"
                @click.stop="joinClub(club.name)"
              >
                Join
              </button>
  
              <button
                v-else
                class="btn bg-red-500 hover:bg-red-600"
                @click.stop="leaveClub(club.name)"
              >
                Leave
              </button>
            </div>
          </div>
        </div>
  
        <!-- No Clubs Message -->
        <div v-else class="text-gray-500 text-lg mt-10">
          No clubs yet. Be the first to create one!
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { authAxios } from '@/utils/axios'
  import Navbar from '@/components/Navbar.vue'
  import { useToast } from 'vue-toastification'
  
  const clubs = ref([])
  const toast = useToast()
  const router = useRouter()
  
  const showCreate = ref(false)
  const newClubName = ref('')
  const newClubDescription = ref('')
  
  const fetchClubs = async () => {
    try {
      const res = await authAxios.get('/clubs/')
      clubs.value = res.data
    } catch (error) {
      console.error(error)
      toast.error('Failed to load clubs.')
    }
  }
  
  const createClub = async () => {
    if (!newClubName.value.trim()) {
      toast.error('Club name is required.')
      return
    }
  
    try {
      await authAxios.post('/clubs/create/', {
        name: newClubName.value.trim(),
        description: newClubDescription.value.trim(),
      })
      toast.success('Club created successfully!')
      resetCreateModal()
      fetchClubs()
    } catch (error) {
      console.error('Create club error:', error)
      toast.error('Failed to create club.')
    }
  }
  
  const joinClub = async (clubName) => {
    try {
      await authAxios.post(`/clubs/${encodeURIComponent(clubName)}/join/`)
      toast.success(`Successfully joined ${clubName}!`)
      fetchClubs()
    } catch (error) {
      console.error(error)
      toast.error('Failed to join club.')
    }
  }
  
  const leaveClub = async (clubName) => {
    try {
      await authAxios.post(`/clubs/${encodeURIComponent(clubName)}/leave/`)
      toast.success(`Successfully left ${clubName}.`)
      fetchClubs()
    } catch (error) {
      console.error(error)
      toast.error('Failed to leave club.')
    }
  }
  
  const resetCreateModal = () => {
    showCreate.value = false
    newClubName.value = ''
    newClubDescription.value = ''
  }
  
  const goToClub = (clubName) => {
  if (!clubName) {
    toast.error('Invalid club name!')
    return
  }
  router.push(`/clubs/${encodeURIComponent(clubName)}`)
}
  
  onMounted(fetchClubs)
  </script>
  
  <style scoped>
  .input {
    @apply p-3 rounded-xl bg-white/50 backdrop-blur-sm placeholder-gray-500 text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-400;
  }
  
  .btn {
    @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300;
  }
  </style>
  