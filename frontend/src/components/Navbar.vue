<template>
  <nav class="w-full p-4 flex justify-between items-center shadow-md fixed top-0 z-50"
    style="background-color: var(--navbar-bg); backdrop-filter: var(--navbar-blur);">
    
    <!-- Logo - Fixed width to prevent shifting -->
    <div class="flex-shrink-0 w-32">
      <RouterLink to="/main" class="text-2xl font-bold text-primary">
        go4friends
      </RouterLink>
    </div>

    <!-- Global Search Bar - Consistent sizing -->
    <div class="relative flex-1 max-w-md mx-4">
      <form @submit.prevent class="relative w-full">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search users, clubs, events..."
          class="w-full px-4 py-2 rounded-full bg-white/70 text-gray-800 placeholder-gray-500 focus:outline-none input-primary text-sm"
        />
        <button
          type="submit"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-primary"
        >
          🔍
        </button>
      </form>

      <!-- Search Dropdown -->
      <div
        v-if="showDropdown"
        class="absolute left-0 mt-2 w-full bg-white border border-gray-300 rounded-xl shadow-lg z-50"
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
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded text-sm"
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
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded text-sm"
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
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded text-sm"
              >
                {{ event.title }}
              </div>
            </div>
            <!-- Classes -->
            <div v-if="results.classes && results.classes.length" class="p-2 border-t border-gray-200">
              <div class="text-xs text-gray-500 mb-1">Classes</div>
              <div
                v-for="cls in results.classes"
                :key="cls.id"
                @click="goToClass(cls.id)"
                class="px-3 py-2 hover:bg-purple-50 cursor-pointer rounded text-sm"
              >
                {{ cls.descr }} — {{ cls.full_name }}
              </div>
            </div>
          </div>
          <div v-else class="p-4 text-sm text-gray-500 text-center">No results found.</div>
        </template>
      </div>
    </div>

    <!-- Right Side Buttons - Consistent spacing and sizing -->
    <div class="flex items-center space-x-3 flex-shrink-0">
      <RouterLink to="/messages" class="btn whitespace-nowrap">💬 Messages</RouterLink>
      <RouterLink to="/clubs" class="btn whitespace-nowrap">Clubs</RouterLink>
      <RouterLink to="/events" class="btn whitespace-nowrap">Events</RouterLink>
      <RouterLink to="/friends" class="btn whitespace-nowrap">Friends</RouterLink>
      <RouterLink v-if="currentUser || fallbackUsername" :to="`/profile/${(currentUser?.username || fallbackUsername)}`" class="btn whitespace-nowrap">Profile</RouterLink>

      <!-- Notifications -->
      <div class="relative" ref="notiButton">
        <button @click.stop="toggleDropdown" class="btn relative whitespace-nowrap">
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
          class="absolute right-0 mt-2 w-80 bg-white rounded-xl p-4 z-50 space-y-2 max-h-96 overflow-y-auto shadow-2xl"
        >
          <!-- Top Controls -->
          <div class="flex justify-between items-center mb-3">
            <button @click.stop="markAllRead" class="text-xs text-purple-700 font-semibold hover:underline">Mark all read</button>
            <button @click.stop="clearNotifications" class="text-xs text-red-500 font-semibold hover:underline">Clear all</button>
          </div>

          <!-- Notifications -->
          <div v-if="notifications.length === 0" class="text-sm text-gray-500 text-center">No notifications yet</div>
          <div v-else class="space-y-3">
            <div
              v-for="notif in notifications"
              :key="notif.id"
              class="flex flex-col bg-gray-100 p-3 rounded-lg hover:bg-gray-200 transition"
            >
              <div class="flex justify-between items-start">
                <div class="text-gray-800 text-sm">{{ notif.message }}</div>
                <button
                  v-if="!notif.is_read"
                  @click.stop="markOneRead(notif.id)"
                  class="text-xs text-blue-600 hover:text-blue-800 font-semibold ml-2"
                >
                  ✓
                </button>
              </div>

              <div v-if="notif.type === 'friend_request'" class="flex justify-end gap-2 mt-2">
                <button @click.stop="acceptFriendFromNotif(notif)" class="greenbtn text-xs">Accept</button>
                <button
                  class="redbtn text-xs font-semibold"
                  @click="rejectFriendFromNotif(notif)"
                >
                  Reject
                </button>
              </div>
              
            </div>
          </div>
        </div>
      </div>

      <RouterLink to="/settings" class="btn whitespace-nowrap">Settings</RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import { useUserStore } from '@/stores/user'

const toast = useToast()
const router = useRouter()
const userStore = useUserStore()

const fallbackUsername = localStorage.getItem('currentUsername')

const searchQuery = ref('')
const showDropdown = ref(false)
const loading = ref(false)
const results = ref({ users: [], clubs: [], events: [] })
const showNotifs = ref(false)
const notiButton = ref(null)
let searchTimeout = null

// Search handlers
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
  router.push(`/events`) // (or `/events/${id}` if you add event detail pages)
}

const goToClass = (id) => {
  showDropdown.value = false
  router.push(`/classes/${id}`) // or wherever your class detail page lives
}

// Notifications handlers
const toggleDropdown = async () => {
  showNotifs.value = !showNotifs.value
  if (showNotifs.value) {
    await userStore.fetchNotifications()
  }
}

const handleClickOutside = (event) => {
  if (notiButton.value && !notiButton.value.contains(event.target)) {
    showNotifs.value = false
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

const acceptFriendFromNotif = async (notif) => {
  try {
    await authAxios.post('/friends/accept/', {
      from_username: extractUsernameFromMessage(notif.message),
    })
    toast.success('Friend request accepted!')

    // 🛠 Remove the notification locally
    userStore.notifications = userStore.notifications.filter(n => n.id !== notif.id)
    userStore.unreadCount = userStore.notifications.filter(n => !n.is_read).length

  } catch (error) {
    toast.error('Error accepting friend request')
  }
}


const rejectFriendFromNotif = async (notif) => {
  try {
    await authAxios.post('/friends/reject/', {
      from_username: extractUsernameFromMessage(notif.message),
    })
    toast.success('Friend request rejected!')

    // 🛠 Remove the notification locally
    userStore.notifications = userStore.notifications.filter(n => n.id !== notif.id)
    userStore.unreadCount = userStore.notifications.filter(n => !n.is_read).length

  } catch (error) {
    toast.error('Error rejecting friend request')
  }
}

const extractUsernameFromMessage = (message) => {
  return message.split(' ')[0]
}

// Computed values
const currentUser = computed(() => userStore.currentUser)
const notifications = computed(() => userStore.notifications)
const unreadCount = computed(() => userStore.unreadCount)

// Mount and cleanup
onMounted(() => {
  userStore.fetchCurrentUser()
  userStore.fetchNotifications()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Ensure consistent button sizing across screen sizes */
.btn {
  @apply px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200;
  min-width: fit-content;
}

.greenbtn {
  @apply bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 transition-colors;
}

.redbtn {
  @apply bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600 transition-colors;
}

/* Prevent layout shifts on different screen sizes */
nav {
  min-height: 64px;
}

/* Ensure search dropdown doesn't cause layout issues */
.relative {
  position: relative;
}

/* Consistent spacing for all screen sizes */
@media (min-width: 1024px) {
  .btn {
    @apply px-4 py-2;
  }
}

@media (min-width: 1280px) {
  nav {
    @apply px-6;
  }
}
</style>