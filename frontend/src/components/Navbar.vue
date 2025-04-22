<template>
  <nav class="w-full p-4 flex justify-between items-center bg-white/30 backdrop-blur-md shadow-md fixed top-0 z-50">
    <RouterLink to="/main" class="text-2xl font-bold text-purple-700">
      whatsurmajor
    </RouterLink>

    <div class="flex space-x-4 items-center relative">
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
import { ref, onMounted } from 'vue'
import { authAxios } from '@/utils/axios'
import { useToast } from 'vue-toastification'

const currentUser = ref(null)
const notifications = ref([])
const unreadCount = ref(0)
const showNotifs = ref(false)
const toast = useToast()

const fetchCurrentUser = async () => {
  try {
    const res = await authAxios.get('/users/me/')
    currentUser.value = res.data
  } catch (error) {
    console.error('Failed to fetch current user:', error)
  }
}

const fetchNotifications = async () => {
  try {
    const res = await authAxios.get('/notifications/')
    notifications.value = res.data
    unreadCount.value = res.data.filter(n => !n.is_read).length
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  }
}

const markAllRead = async () => {
  try {
    await authAxios.post('/notifications/mark-read/')
    toast.success('All notifications marked as read')
    fetchNotifications()
  } catch (error) {
    console.error('Failed to mark notifications as read:', error)
    toast.error('Failed to mark as read')
  }
}

const clearNotifications = async () => {
  try {
    await authAxios.post('/notifications/clear/')
    toast.success('All notifications cleared')
    notifications.value = []
    unreadCount.value = 0
  } catch (error) {
    console.error('Failed to clear notifications:', error)
    toast.error('Failed to clear notifications')
  }
}

const toggleDropdown = () => {
  showNotifs.value = !showNotifs.value
  if (showNotifs.value) {
    fetchNotifications()
  }
}

const acceptFriendFromNotif = async (notif) => {
  try {
    await authAxios.post('/friends/accept/', {
      from_username: extractUsernameFromMessage(notif.message),
    })
    toast.success('Friend request accepted!')
    await authAxios.post('/notifications/mark-read/')  // Optional if you want to mark it
    fetchNotifications()
  } catch (error) {
    console.error('Failed to accept friend request:', error)
    toast.error('Error accepting friend request.')
  }
}

const extractUsernameFromMessage = (message) => {
  // Assumes the message is like "brocoder sent you a friend request!"
  return message.split(' ')[0]
}

const markOneRead = async (id) => {
  try {
    await authAxios.post(`/notifications/${id}/mark-read/`)
    toast.success('Marked as read')
    fetchNotifications()
  } catch (error) {
    console.error('Failed to mark notification as read:', error)
    toast.error('Failed to mark as read')
  }
}


onMounted(() => {
  fetchCurrentUser()
  fetchNotifications()
})

</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-xl text-base transition-all duration-300;
}
</style>