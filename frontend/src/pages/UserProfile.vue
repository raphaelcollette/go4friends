<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div v-if="loading" class="text-gray-600 text-lg">Loading profile...</div>

      <div v-else-if="!user" class="text-gray-500 text-lg">User not found.</div>

      <div v-else class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 max-w-md w-full text-center">
        <div class="flex justify-center">
          <img
            v-if="user.profile_picture"
            :src="user.profile_picture"
            alt="Profile Picture"
            class="w-28 h-28 rounded-full object-cover border-4 border-purple-300"
          />
          <div v-else class="w-28 h-28 rounded-full bg-purple-200 flex items-center justify-center text-4xl text-white">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>
        </div>

        <h1 class="text-3xl font-bold text-gray-800 mt-6">{{ user.full_name || user.username }}</h1>
        <p class="text-gray-600 mt-2">@{{ user.username }}</p>

        <p v-if="user.bio" class="mt-4 text-gray-700 italic">{{ user.bio }}</p>
        <p v-if="user.location" class="mt-2 text-gray-500 text-sm">📍 {{ user.location }}</p>

        <!-- Friend Button Section -->
        <div class="mt-6">
          <template v-if="user.username !== currentUsername">
            <button
              v-if="user.is_friend"
              @click="removeFriend"
              class="btn bg-red-500 hover:bg-red-600"
            >
              Unfriend
            </button>
            <button
              v-else-if="user.friend_request_sent"
              class="btn bg-yellow-500 hover:bg-yellow-600 cursor-default"
              disabled
            >
              Request Sent
            </button>
            <button
              v-else
              @click="sendFriendRequest"
              class="btn bg-purple-600 hover:bg-purple-700"
            >
              + Add Friend
            </button>
          </template>
        </div>

        <!-- Message Button -->
        <div class="mt-4" v-if="user.username !== currentUsername">
          <RouterLink
            :to="`/messages/thread/${user.username}`"
            class="btn bg-blue-500 hover:bg-blue-600"
          >
            💬 Message
          </RouterLink>
        </div>

        <!-- Clubs Section -->
        <div v-if="user.clubs?.length" class="mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Clubs</h2>
          <div class="flex flex-wrap justify-center gap-2">
            <RouterLink
              v-for="club in user.clubs"
              :key="club.id"
              :to="`/clubs/${encodeURIComponent(club.name)}`"
              class="bg-purple-100 text-purple-700 text-sm font-semibold px-3 py-1 rounded-full hover:bg-purple-200 transition-all"
            >
              {{ club.name }}
            </RouterLink>
          </div>
        </div>

        <!-- Interests Section -->
        <div v-if="user.interests?.length" class="mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Interests</h2>
          <div class="flex flex-wrap justify-center gap-2">
            <span
              v-for="(interest, idx) in user.interests"
              :key="idx"
              class="bg-green-100 text-green-700 text-sm font-semibold px-3 py-1 rounded-full"
            >
              {{ interest }}
            </span>
          </div>
        </div>

        <p v-if="user.major" class="mt-2 text-gray-600 text-sm">🎓 Major: {{ user.major }}</p>
        <p v-if="user.graduation_year" class="text-gray-600 text-sm">🎓 Class of {{ user.graduation_year }}</p>

        <div class="mt-6 flex justify-center space-x-4">
          <RouterLink to="/friends" class="btn">Back to Friends</RouterLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const user = ref(null)
const loading = ref(true)
const toast = useToast()
const currentUsername = ref('')

// Fetch profile user
const fetchUser = async () => {
  try {
    loading.value = true
    const username = route.params.username
    const res = await authAxios.get(`users/profile/${username}/`)
    user.value = res.data

    const me = await authAxios.get('/users/me/')
    currentUsername.value = me.data.username
  } catch (error) {
    console.error('Failed to fetch user:', error)
    toast.error('Failed to load user profile.')
    user.value = null
  } finally {
    loading.value = false
  }
}

// Send Friend Request
const sendFriendRequest = async () => {
  try {
    await authAxios.post('/friends/send/', { to_username: user.value.username })
    toast.success('Friend request sent!')
    user.value.friend_request_sent = true
  } catch (error) {
    console.error('Failed to send friend request:', error)
    toast.error('Failed to send friend request.')
  }
}

// Remove Friend
const removeFriend = async () => {
  try {
    await authAxios.post('/friends/remove/', { username: user.value.username })
    toast.success('Friend removed.')
    user.value.is_friend = false
  } catch (error) {
    console.error('Failed to remove friend:', error)
    toast.error('Failed to remove friend.')
  }
}

// Initial fetch
onMounted(fetchUser)
watch(() => route.params.username, fetchUser)
</script>

<style scoped>
.btn {
  @apply text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
</style>


