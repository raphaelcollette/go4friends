<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div v-if="loading" class="text-gray-600 text-lg">Loading profile...</div>

      <!-- Private Profile Message -->
      <div v-else-if="user?.private" class="bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 max-w-md w-full text-center">
        <h2 class="text-2xl font-bold text-gray-800">🔒 Private Profile</h2>
        <p class="text-gray-600 mt-2">This user's profile is private and only visible to friends.</p>
      </div>

      <!-- User Not Found Message -->
      <div v-else-if="!user" class="bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 max-w-md w-full text-center">
        <h2 class="text-2xl font-bold text-gray-800">❌ User Not Found</h2>
        <p class="text-gray-600 mt-2">We couldn't find anyone with that username.</p>
      </div>

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

        <!-- Message button -->
        <div class="mt-4" v-if="user.username !== currentUsername">
          <button
            @click="startOrNavigateToThread"
            class="btn bg-blue-500 hover:bg-blue-600"
          >
            💬 Message
          </button>
        </div>

        <!-- Clubs -->
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

        <!-- Interests -->
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

const fetchUser = async () => {
  loading.value = true
  const username = route.params.username

  try {
    // Always fetch current user once and store the username
    if (!currentUsername.value) {
      const me = await authAxios.get('/users/me/')
      currentUsername.value = me.data.username
    }

    // Use /me/ endpoint if viewing your own profile
    const res = username === currentUsername.value
      ? await authAxios.get('/users/me/')
      : await authAxios.get(`/users/profile/${username}/`)

    user.value = res.data
  } catch (error) {
    if (error.response?.status === 403) {
      user.value = { private: true }
    } else {
      toast.error('Failed to load user profile.')
      user.value = null
    }
  } finally {
    loading.value = false
  }
}

const sendFriendRequest = async () => {
  try {
    await authAxios.post('/friends/send/', { to_username: user.value.username })
    toast.success('Friend request sent!')
    user.value.friend_request_sent = true
  } catch (error) {
    toast.error('Failed to send friend request.')
  }
}

const removeFriend = async () => {
  try {
    await authAxios.post('/friends/remove/', { username: user.value.username })
    toast.success('Friend removed.')
    user.value.is_friend = false
  } catch (error) {
    toast.error('Failed to remove friend.')
  }
}

const startOrNavigateToThread = async () => {
  try {
    const res = await authAxios.post('/messages/threads/start-private/', {
      username: user.value.username
    })
    const threadId = res.data.thread_id
    router.push(`/messages/thread/${threadId}`)
  } catch (e) {
    toast.error('Could not start chat.')
  }
}

onMounted(fetchUser)
watch(() => route.params.username, fetchUser)
</script>

<style scoped>
.btn {
  @apply text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
</style>


