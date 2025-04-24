<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <!-- Loading -->
      <div v-if="loading" class="text-gray-600 text-lg">Loading club...</div>

      <!-- Club Found -->
      <div v-else-if="club && club.name" class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 w-full max-w-4xl text-center">
        <h1 class="text-4xl font-bold text-gray-800 mb-6">{{ club.name }}</h1>

        <p class="text-gray-600 italic mb-10">
          {{ club.description || 'No description available.' }}
        </p>

        <h2 class="text-2xl font-bold text-gray-800 mb-6">Members</h2>

        <div v-if="members.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="member in members"
            :key="member.id"
            @click="goToProfile(member.user.username)"
            class="flex flex-col items-center bg-white/30 backdrop-blur-md p-4 rounded-xl hover:bg-white/50 transition-all cursor-pointer"
          >
            <div class="w-20 h-20 rounded-full overflow-hidden flex items-center justify-center bg-purple-200">
              <img
                v-if="member.user.profile_picture"
                :src="member.user.profile_picture"
                alt="Profile Picture"
                class="w-full h-full object-cover"
              />
              <div v-else class="text-2xl text-white font-bold">
                {{ member.user.username?.charAt(0).toUpperCase() }}
              </div>
            </div>
            <p class="mt-3 font-semibold text-gray-800">
              {{ member.user.username }}
              <span v-if="member.is_owner" class="text-purple-600 text-sm font-bold">(Owner)</span>
            </p>
          </div>
        </div>

        <div v-else class="text-gray-500 text-lg mt-4">
          No members yet!
        </div>
      </div>

      <!-- Club Not Found -->
      <div v-else class="text-center text-lg text-gray-500 mt-10">
        ❌ Club not found.
      </div>
    </main>
  </div>
</template>

  
<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useClubStore } from '@/stores/club'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const clubStore = useClubStore()

const clubName = decodeURIComponent(route.params.clubName)

const club = computed(() => clubStore.currentClub)
const members = computed(() => clubStore.clubMembers)
const loading = computed(() => clubStore.loadingClub)

const goToProfile = (username) => {
  router.push(`/profile/${username}`)
}

onMounted(async () => {
  try {
    await clubStore.fetchClubProfile(clubName)
  } catch (error) {
    toast.error('Could not load club.')
  }
})
</script>
  
  <style scoped>
  .btn {
    @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
  }
  </style>
  
  
  