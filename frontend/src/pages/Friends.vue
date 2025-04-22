<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />
    <!-- Remove Friend Modal -->
    <div v-if="removingUser" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm text-center space-y-6 shadow-lg">
        <h2 class="text-xl font-bold text-gray-800">Remove Friend?</h2>
        <p class="text-gray-600">Are you sure you want to remove <span class="font-semibold">@{{ removingUser }}</span> from your friends?</p>

        <div class="flex justify-center space-x-4">
          <button class="btn bg-gray-300 hover:bg-gray-400 text-gray-800" @click="removingUser = null">Cancel</button>
          <button class="btn bg-red-500 hover:bg-red-600" @click="confirmRemoveFriend">Remove</button>
        </div>
      </div>
    </div>
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div class="w-full max-w-6xl flex justify-between items-center mb-10">
        <h1 class="text-4xl font-extrabold text-gray-800">Your Friends</h1>

        <div class="flex space-x-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search users..."
            class="input"
          />
          <button class="btn" @click="searchUsers">Search</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-gray-600 text-lg">Loading friends...</div>

      
      <!-- Search Results -->
      <div v-else-if="searchResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl mb-16">
        <RouterLink
          v-for="user in searchResults"
          :key="user.id"
          :to="`/profile/${user.username}`"
          class="flex flex-col items-center p-6 bg-white/20 backdrop-blur-md rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group cursor-pointer"
        >
          <div v-if="user.profile_picture">
            <img
              :src="user.profile_picture"
              alt="Profile Picture"
              class="w-24 h-24 rounded-full object-cover border-4 border-purple-300"
            />
          </div>
          <div v-else class="w-24 h-24 rounded-full bg-purple-200 flex items-center justify-center text-3xl text-white">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>

          <p class="mt-4 text-lg font-semibold text-gray-800">{{ user.full_name || user.username }}</p>
          <p class="text-sm text-gray-600">@{{ user.username }}</p>
        </RouterLink>
      </div>

      <!-- Pending Requests -->
      <div v-if="pendingRequests.length > 0" class="w-full max-w-6xl mb-16">
        <h2 class="text-2xl font-bold text-gray-700 mb-6">Pending Friend Requests</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <div
            v-for="request in pendingRequests"
            :key="request.id"
            class="flex flex-col items-center p-6 bg-white/20 backdrop-blur-md rounded-2xl shadow-md hover:shadow-xl transition-all duration-300"
          >
            <!-- 👇 Fix: Proper profile picture check -->
            <div v-if="request.from_profile_picture">
              <img
                :src="request.from_profile_picture"
                alt="Profile Picture"
                class="w-20 h-20 rounded-full object-cover border-4 border-purple-300"
              />
            </div>
            <div v-else class="w-20 h-20 rounded-full bg-purple-200 flex items-center justify-center text-3xl text-white">
              {{ request.from_username.charAt(0).toUpperCase() }}
            </div>

            <p class="mt-4 text-lg font-semibold text-gray-800">{{ request.from_username }}</p>

            <div class="flex space-x-4 mt-4">
              <button class="btn bg-green-500 hover:bg-green-600" @click="acceptRequest(request.from_username)">Accept</button>
              <button class="btn bg-red-500 hover:bg-red-600" @click="rejectRequest(request.from_username)">Reject</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Friends -->
      <div v-if="friends.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl">
        <RouterLink
          v-for="friend in friends"
          :key="friend.id"
          :to="`/profile/${friend.username}`"
          class="flex flex-col items-center p-6 bg-white/20 backdrop-blur-md rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group"
        >
          <div v-if="friend.profile_picture">
            <img
              :src="friend.profile_picture"
              alt="Profile Picture"
              class="w-24 h-24 rounded-full object-cover border-4 border-purple-300"
            />
          </div>
          <div v-else class="w-24 h-24 rounded-full bg-purple-200 flex items-center justify-center text-3xl text-white">
            {{ friend.username.charAt(0).toUpperCase() }}
          </div>

          <p class="mt-4 text-lg font-semibold text-gray-800">{{ friend.full_name || friend.username }}</p>
          <p class="text-sm text-gray-600">@{{ friend.username }}</p>

          <!-- Remove Button (appears on hover) -->
          <button
            @click.stop.prevent="removeFriend(friend.username)"
            class="hidden group-hover:block absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white text-xs font-bold py-1 px-2 rounded"
          >
            Remove
          </button>
        </RouterLink>
      </div>

      <!-- No Friends -->
      <div v-else-if="!loading && friends.length === 0" class="text-gray-500 text-lg mt-10">
        You have no friends yet.
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
const pendingRequests = ref([])
const loading = ref(true)
const toast = useToast()

const searchQuery = ref('')
const searchResults = ref([])

const fetchFriends = async () => {
  loading.value = true
  try {
    const res = await authAxios.get('friends/friends/')
    friends.value = res.data

    const pendingRes = await authAxios.get('friends/requests/')
    pendingRequests.value = pendingRes.data
  } catch (error) {
    console.error('Failed to fetch friends or requests:', error)
    toast.error('Failed to load friends.')
  } finally {
    loading.value = false
  }
}

const searchUsers = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  try {
    const res = await authAxios.get(`users/search/?q=${searchQuery.value}`)
    searchResults.value = res.data
  } catch (error) {
    console.error('Search failed:', error)
    toast.error('Search failed.')
  }
}

const sendFriendRequest = async (username) => {
  try {
    await authAxios.post('friends/send/', { to_username: username })
    toast.success(`Friend request sent to ${username}!`)
    searchQuery.value = ''
    searchResults.value = []
  } catch (error) {
    console.error('Failed to send friend request:', error)
    toast.error('Failed to send friend request.')
  }
}

const acceptRequest = async (fromUsername) => {
  try {
    await authAxios.post('friends/accept/', { from_username: fromUsername })
    toast.success(`Friend request accepted from ${fromUsername}!`)
    fetchFriends()
  } catch (error) {
    console.error('Failed to accept friend request:', error)
    toast.error('Failed to accept request.')
  }
}

const rejectRequest = async (fromUsername) => {
  try {
    await authAxios.post('friends/reject/', { from_username: fromUsername })
    toast.success(`Friend request rejected from ${fromUsername}.`)
    fetchFriends()
  } catch (error) {
    console.error('Failed to reject friend request:', error)
    toast.error('Failed to reject request.')
  }
}

const removingUser = ref(null)

const removeFriend = (username) => {
  removingUser.value = username
}

const confirmRemoveFriend = async () => {
  if (!removingUser.value) return

  try {
    await authAxios.post('friends/remove/', { username: removingUser.value })
    toast.success(`${removingUser.value} has been removed.`)
    removingUser.value = null
    fetchFriends()
  } catch (error) {
    console.error('Failed to remove friend:', error)
    toast.error('Failed to remove friend.')
  }
}

onMounted(fetchFriends)
</script>

<style scoped>
.input {
  @apply bg-white border border-gray-300 rounded-xl p-3 text-base focus:outline-none focus:ring-2 focus:ring-purple-400 w-48;
}

.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300 text-base;
}
</style>

