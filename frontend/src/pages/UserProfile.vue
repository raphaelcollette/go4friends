<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      
      <!-- Loading State -->
      <div v-if="loading" class="text-gray-600 text-lg">Loading profile...</div>

      <!-- Private Profile -->
      <div v-else-if="user?.private" class="glossy-bg rounded-2xl shadow-md p-6 max-w-md w-full text-center">
        <h2 class="text-2xl font-bold text-gray-800">🔒 Private Profile</h2>
        <p class="text-gray-600 mt-2">This user's profile is private and only visible to friends.</p>
      </div>

      <!-- User Not Found -->
      <div v-else-if="!user" class="glossy-bg rounded-2xl shadow-md p-6 max-w-md w-full text-center">
        <h2 class="text-2xl font-bold text-gray-800">❌ User Not Found</h2>
        <p class="text-gray-600 mt-2">We couldn't find anyone with that username.</p>
      </div>

      <!-- Profile Card -->
      <div v-else class="glossy-bg rounded-2xl shadow-lg p-8 max-w-md w-full text-center">
        <div class="flex justify-center">
          <img
            v-if="user.profile_picture"
            :src="user.profile_picture"
            alt="Profile Picture"
            class="w-28 h-28 rounded-full object-cover border-4"
            :style="{ borderColor: 'var(--btn-primary, #6366f1)' }"
          />
          <div v-else class="w-28 h-28 rounded-full flex items-center justify-center text-4xl text-white"
            :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>
        </div>

        <h1 class="text-3xl font-bold text-gray-800 mt-6">{{ user.full_name || user.username }}</h1>
        <p class="text-gray-600 mt-2">@{{ user.username }}</p>

        <p v-if="user.bio" class="mt-4 text-gray-700 italic">{{ user.bio }}</p>
        <p v-if="user.location" class="text-gray-500 text-sm mt-2">📍 {{ user.location }}</p>

        <!-- Friend Actions -->
        <div class="mt-6" v-if="!isCurrentUser">
          <button v-if="user.is_friend" @click="removeFriend" class="redbtn">Unfriend</button>
          <button v-else-if="user.friend_request_sent" class="btn" disabled>Request Sent</button>
          <button v-else @click="sendFriendRequest" class="btn">+ Add Friend</button>

          <div class="mt-4">
            <button @click="startOrNavigateToThread" class="btn">💬 Message</button>
          </div>
        </div>

        <!-- Clubs -->
        <div v-if="user.clubs?.length" class="mt-8">
          <h2 class="text-xl font-bold text-gray-800 mb-4">Clubs</h2>
          <div class="flex flex-wrap justify-center gap-2">
            <RouterLink
              v-for="club in user.clubs"
              :key="club.id"
              :to="`/clubs/${encodeURIComponent(club.name)}`"
              class="bg-purple-100 text-purple-700 text-sm font-semibold px-3 py-1 rounded-full hover:bg-purple-200 transition"
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
              class="text-sm font-semibold px-3 py-1 rounded-full"
              :style="{
                backgroundColor: 'var(--btn-secondary, #a5b4fc)',
                color: 'var(--btn-primary, #6366f1)',
              }"
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
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const user = ref(null)
const loading = ref(true)

const isCurrentUser = computed(() => {
  return userStore.currentUser && user.value && userStore.currentUser.username === user.value.username
})

const fetchUser = async () => {
  loading.value = true
  const username = route.params.username
  const now = Date.now()
  const oneMinute = 60 * 1000

  try {
    // Check cache from userStore
    const cached = userStore.profileCache[username]

    if (cached && (now - cached.lastFetched) < oneMinute) {
      // 
      user.value = cached.data
    } else {
      // 
      const res = await authAxios.get(`/users/profile/${username}/`)
      user.value = res.data

      // 
      userStore.profileCache[username] = {
        data: res.data,
        lastFetched: now
      }

      // 
      if (userStore.currentUser && username === userStore.currentUser.username) {
        userStore.currentUser = res.data
        localStorage.setItem('currentUser', JSON.stringify(res.data))
      }
    }
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
      username: user.value.username,
    })
    const threadId = res.data.thread_id
    
    // Navigate to messages with thread selection
    router.push(`/messages?thread=${threadId}`)
  } catch (e) {
    toast.error('Could not start chat.')
  }
}

onMounted(fetchUser)
watch(() => route.params.username, fetchUser)
</script>

<style scoped>
</style>


