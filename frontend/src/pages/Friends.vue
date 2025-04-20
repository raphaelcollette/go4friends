<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <h1 class="text-4xl font-extrabold text-gray-800 mb-8">Your Friends</h1>

      <div v-if="loading" class="text-gray-600">Loading friends...</div>

      <div v-else-if="friends.length === 0" class="text-gray-500">You have no friends yet.</div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-5xl">
        <div v-for="friend in friends" :key="friend.id" class="flex flex-col items-center p-4 bg-white/20 backdrop-blur-md rounded-2xl shadow-md">
          <img
            v-if="friend.profile_picture"
            :src="friend.profile_picture"
            alt="Profile Picture"
            class="w-24 h-24 rounded-full object-cover border-4 border-purple-300"
          />
          <div v-else class="w-24 h-24 rounded-full bg-purple-200 flex items-center justify-center text-3xl text-white">
            {{ friend.username.charAt(0).toUpperCase() }}
          </div>

          <p class="mt-4 font-semibold text-gray-800">{{ friend.username }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

const friends = ref([])
const loading = ref(true)
const toast = useToast()

const fetchFriends = async () => {
  try {
    const res = await authAxios.get('friends/friends/')
    friends.value = res.data
  } catch (error) {
    console.error('Failed to fetch friends:', error)
    toast.error('Failed to load friends.')
  } finally {
    loading.value = false
  }
}

onMounted(fetchFriends)
</script>

<style scoped>
/* No extra styles needed; Tailwind handles it */
</style>
