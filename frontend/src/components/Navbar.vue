<template>
  <nav class="w-full p-4 flex justify-between items-center bg-white/30 backdrop-blur-md shadow-md fixed top-0 z-50">
    <RouterLink to="/main" class="text-2xl font-bold text-purple-700">
      placeholder
    </RouterLink>

    <!-- Global Search Bar -->
<div class="flex-1 mx-8 relative">
  <form @submit.prevent class="relative w-full max-w-md mx-auto">
    <input
      v-model="searchQuery"
      @input="handleSearch"
      type="text"
      placeholder="Search users, clubs, events..."
      class="w-full px-4 py-2 rounded-full bg-white/70 text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-400"
    />
    <button
      type="submit"
      class="absolute right-2 top-1/2 transform -translate-y-1/2 text-purple-600 hover:text-purple-800"
    >
      🔍
    </button>
  </form>

  <!-- Search Dropdown -->
  <div
    v-if="showDropdown"
    class="absolute mt-2 w-full max-w-md bg-white border border-gray-300 rounded-xl shadow-lg z-50"
      >
        <div v-if="loading" class="p-4 text-center text-gray-500">Searching...</div>

        <template v-else>
          <div v-if="hasResults">
            <!-- Users -->
            <div v-if="results.users.length" class="p-2 border-b border-gray-200">
              <div class="text-xs text-gray-500 mb-1">Users</div>
              <div
                v-for="user in results.users"
                :key="user.username"
                @click="goToUser(user.username)"
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded"
              >
                @{{ user.username }} <span v-if="user.full_name">– {{ user.full_name }}</span>
              </div>
            </div>

            <!-- Clubs -->
            <div v-if="results.clubs.length" class="p-2 border-b border-gray-200">
              <div class="text-xs text-gray-500 mb-1">Clubs</div>
              <div
                v-for="club in results.clubs"
                :key="club.id"
                @click="goToClub(club.name)"
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded"
              >
                {{ club.name }}
              </div>
            </div>

            <!-- Events -->
            <div v-if="results.events.length" class="p-2">
              <div class="text-xs text-gray-500 mb-1">Events</div>
              <div
                v-for="event in results.events"
                :key="event.id"
                @click="goToEvent(event.id)"
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded"
              >
                {{ event.title }}
              </div>
            </div>
          </div>

          <div v-else class="p-4 text-sm text-gray-500 text-center">No results found.</div>
        </template>
      </div>
    </div>


    <div class="flex space-x-4 items-center relative">
      <RouterLink
        to="/messages"
        class="btn"
      >
        💬 Messages
      </RouterLink>
      <RouterLink to="/clubs" class="btn">Clubs</RouterLink>
      <RouterLink to="/events" class="btn">Events</RouterLink>
      <RouterLink to="/friends" class="btn">Friends</RouterLink>

      <!-- Profile & Settings -->
      <RouterLink
        v-if="currentUser"
        :to="`/profile/${currentUser.username}`"
        class="btn"
      >
        Profile
      </RouterLink>
      <!-- Notification Dropdown -->
      <div class="relative">
        <button @click="toggleDropdown" class="btn relative">
          🔔
          <span
            v-if="unreadCount > 0"
            class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
          >
            {{ unreadCount }}
          </span>
        </button>

        <div
          v-if="showNotifs"
          class="absolute right-0 mt-2 w-80 bg-white shadow-lg rounded-xl p-4 z-50 space-y-2 max-h-96 overflow-y-auto"
        >
          <!-- Control Buttons -->
          <div class="flex justify-between items-center mb-2">
            <button
              @click="markAllRead"
              class="text-xs text-purple-700 font-semibold hover:underline"
            >
              Mark all as read
            </button>
            <button
              @click="clearNotifications"
              class="text-xs text-red-500 font-semibold hover:underline"
            >
              Clear all
            </button>
          </div>

          <!-- Notification List -->
          <div v-if="notifications.length === 0" class="text-sm text-gray-500">No notifications</div>
          <div
            v-for="notif in notifications"
            :key="notif.id"
            class="text-sm text-gray-800 bg-purple-50 px-3 py-2 rounded hover:bg-purple-100 transition"
          >
            <div class="flex justify-between items-center">
              <span>{{ notif.message }}</span>

              <button
                v-if="!notif.is_read"
                @click="markOneRead(notif.id)"
                class="text-xs text-blue-600 hover:text-blue-800 font-semibold ml-4"
              >
                Mark Read
              </button>
            </div>

            <!-- Optional: friend request logic -->
            <div v-if="notif.type === 'friend_request'" class="mt-2 flex justify-end">
              <button
                class="text-xs font-semibold text-green-600 hover:text-green-800"
                @click="acceptFriendFromNotif(notif)"
              >
                Accept Friend
              </button>
            </div>
          </div>
        </div>
    </div>


      <RouterLink to="/settings" class="btn">Settings</RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import { useUserStore } from '@/stores/user' // ✅ import Pinia store

const toast = useToast()
const router = useRouter()
const userStore = useUserStore() // ✅ store instance

// ✅ Search functionality
const searchQuery = ref('')
const showDropdown = ref(false)
const loading = ref(false)
const results = ref({ users: [], clubs: [], events: [] })
let searchTimeout = null

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    showDropdown.value = false
    return
  }

  loading.value = true
  showDropdown.value = true

  searchTimeout = setTimeout(async () => {
    try {
      const res = await authAxios.get(`/search/?q=${encodeURIComponent(searchQuery.value)}`)
      results.value = res.data
    } catch (error) {
      console.error('Search failed', error)
    } finally {
      loading.value = false
    }
  }, 300)
}

const hasResults = computed(() =>
  results.value.users.length || results.value.clubs.length || results.value.events.length
)

const goToUser = (username) => {
  showDropdown.value = false
  router.push(`/profile/${username}`)
}

const goToClub = (clubName) => {
  showDropdown.value = false
  router.push(`/clubs/${encodeURIComponent(clubName)}`)
}

const goToEvent = (id) => {
  showDropdown.value = false
  router.push(`/events`) // change to `/events/${id}` if using detail view
}

// ✅ Notifications
const showNotifs = ref(false)

const toggleDropdown = async () => {
  showNotifs.value = !showNotifs.value
  if (showNotifs.value) {
    await userStore.fetchNotifications()
  }
}

const markAllRead = async () => {
  try {
    await userStore.markAllRead()
    toast.success('All notifications marked as read')
  } catch (error) {
    toast.error('Failed to mark as read')
  }
}

const clearNotifications = async () => {
  try {
    await userStore.clearNotifications()
    toast.success('All notifications cleared')
  } catch (error) {
    toast.error('Failed to clear notifications')
  }
}

const acceptFriendFromNotif = async (notif) => {
  try {
    await authAxios.post('/friends/accept/', {
      from_username: extractUsernameFromMessage(notif.message),
    })
    toast.success('Friend request accepted!')
    await userStore.fetchNotifications()
  } catch (error) {
    toast.error('Error accepting friend request.')
  }
}

const extractUsernameFromMessage = (message) => {
  return message.split(' ')[0]
}

const markOneRead = async (id) => {
  try {
    await authAxios.post(`/notifications/${id}/mark-read/`)
    const notif = userStore.notifications.find(n => n.id === id)
    if (notif) notif.is_read = true
    userStore.unreadCount = userStore.notifications.filter(n => !n.is_read).length
    toast.success('Marked as read')
  } catch (error) {
    toast.error('Failed to mark as read')
  }
}

// ✅ Initial fetch on mount only once
onMounted(() => {
  userStore.fetchCurrentUser()
  userStore.fetchNotifications()
})

// ✅ Expose from store
const currentUser = computed(() => userStore.currentUser)
const notifications = computed(() => userStore.notifications)
const unreadCount = computed(() => userStore.unreadCount)
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-xl text-base transition-all duration-300;
}
</style>