<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div v-if="loading" class="text-gray-600 text-lg">Loading profile...</div>

      <div v-else class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 max-w-md w-full text-center">
        <div class="flex justify-center">
          <img
            v-if="user.profile_picture"
            :src="user.profile_picture"
            alt="Profile Picture"
            class="w-28 h-28 rounded-full object-cover border-4 border-purple-300"
          />
          <div v-else class="w-28 h-28 rounded-full bg-purple-200 flex items-center justify-center text-4xl text-white">
            {{ user.username?.charAt(0).toUpperCase() }}
          </div>
        </div>

        <h1 class="text-3xl font-bold text-gray-800 mt-6">{{ user.full_name || user.username }}</h1>
        <p class="text-gray-600 mt-2">@{{ user.username }}</p>

        <p v-if="user.bio" class="mt-4 text-gray-700 italic">{{ user.bio }}</p>
        <p v-if="user.location" class="mt-2 text-gray-500 text-sm">📍 {{ user.location }}</p>

        <!-- My Clubs Section -->
        <div v-if="clubs.length > 0" class="mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">My Clubs</h2>
          <ul class="space-y-2">
            <li
              v-for="club in clubs"
              :key="club.id"
              class="bg-white/30 rounded-xl p-3 text-gray-700 hover:bg-white/50 transition-all"
            >
              {{ club.name }}
            </li>
          </ul>
        </div>

        <!-- No Clubs Message + Create Button -->
        <div v-else class="mt-8 text-center">
          <p class="text-gray-500 text-sm mb-4">
            You haven't joined any clubs yet.
          </p>
          <button class="btn" @click="goToClubs">
            + Create Your First Club
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'

const user = ref({})
const clubs = ref([])
const loading = ref(true)
const router = useRouter()

const fetchUser = async () => {
  try {
    const res = await authAxios.get('/users/me/')
    user.value = res.data
  } catch (error) {
    console.error('Failed to fetch profile:', error)
    router.push('/login')
  }
}

const fetchMyClubs = async () => {
  try {
    const res = await authAxios.get('/clubs/')
    clubs.value = res.data.filter(club => club.is_member)
  } catch (error) {
    console.error('Failed to fetch clubs:', error)
  }
}

const goToClubs = () => {
  router.push('/clubs')  // assumes you have a /clubs route
}

onMounted(async () => {
  await fetchUser()
  await fetchMyClubs()
  loading.value = false
})
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
</style>
