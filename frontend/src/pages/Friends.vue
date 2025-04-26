<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">

    <!-- Remove Friend Modal -->
    <div v-if="removingUser" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm text-center space-y-6 shadow-lg">
        <h2 class="text-xl font-bold text-gray-800">Remove Friend?</h2>
        <p class="text-gray-600">Are you sure you want to remove <span class="font-semibold">@{{ removingUser }}</span> from your friends?</p>
        <div class="flex justify-center space-x-4">
          <button class="btn" @click="removingUser = null">Cancel</button>
          <button class="redbtn" @click="confirmRemoveFriend">Remove</button>
        </div>
      </div>
    </div>

    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      
      <!-- Header -->
      <div class="w-full max-w-6xl flex justify-between items-center mb-10">
        <h1 class="text-4xl font-extrabold text-gray-800">Your Friends</h1>
        <div class="flex space-x-4">
          <input v-model="searchQuery" type="text" placeholder="Search users..." class="input" />
          <button class="btn" @click="searchUsers">Search</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="friendStore.loading" class="text-gray-600 text-lg">Loading friends...</div>

      <!-- Search Results -->
      <div v-else-if="friendStore.searchResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl mb-16">
        <RouterLink
          v-for="user in friendStore.searchResults"
          :key="user.id"
          :to="`/profile/${user.username}`"
          class="flex flex-col items-center p-6 glossy-bg rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group cursor-pointer"
        >
          <div v-if="user.profile_picture">
            <img :src="user.profile_picture" alt="Profile Picture" class="w-24 h-24 rounded-full object-cover border-4 border-purple-300" />
          </div>
          <div
            v-else
            class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white"
            :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
          >
            {{ user?.username?.charAt(0)?.toUpperCase() }}
          </div>
          <p class="mt-4 text-lg font-semibold text-gray-800">{{ user.full_name || user.username }}</p>
          <p class="text-sm text-gray-600">@{{ user.username }}</p>
        </RouterLink>
      </div>

      <!-- Pending Requests -->
      <div v-if="friendStore.pendingRequests.length > 0" class="w-full max-w-6xl mb-16">
        <h2 class="text-2xl font-bold text-gray-700 mb-6">Pending Friend Requests</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <div
            v-for="request in friendStore.pendingRequests"
            :key="request.id"
            class="flex flex-col items-center p-6 glossy-bg rounded-2xl shadow-md hover:shadow-xl transition-all duration-300"
          >
            <div v-if="request.from_profile_picture">
              <img :src="request.from_profile_picture" alt="Profile Picture" class="w-20 h-20 rounded-full object-cover border-4 border-purple-300" />
            </div>
            <div
              v-else
              class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white"
              :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
            >
              {{ request?.from_username?.charAt(0)?.toUpperCase() }}
            </div>
            <p class="mt-4 text-lg font-semibold text-gray-800">{{ request.from_username }}</p>
            <div class="flex space-x-4 mt-4">
              <button class="greenbtn" @click="friendStore.acceptRequest(request.from_username)">Accept</button>
              <button class="redbtn" @click="friendStore.rejectRequest(request.from_username)">Reject</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Suggested Friends -->
      <div v-if="friendStore.suggested.length > 0" class="w-full max-w-6xl mb-16">
        <h2 class="text-2xl font-bold text-gray-700 mb-6">Suggested Friends</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <RouterLink
            v-for="user in friendStore.suggested"
            :key="user.id"
            :to="`/profile/${user.username}`"
            class="flex flex-col items-center p-6 glossy-bg rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group cursor-pointer"
          >
            <div v-if="user.profile_picture">
              <img :src="user.profile_picture" alt="Profile Picture" class="w-24 h-24 rounded-full object-cover border-4" :style="{ borderColor: 'var(--btn-primary, #7C0A02)' }" />
            </div>
            <div
              v-else
              class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white"
              :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
            >
              {{ user?.username?.charAt(0)?.toUpperCase() }}
            </div>

            <p class="mt-4 text-lg font-semibold text-gray-800">{{ user.full_name || user.username }}</p>
            <p class="text-sm text-gray-600">@{{ user.username }}</p>

            <div class="flex flex-wrap justify-center gap-2 mt-2">
              <span
                v-for="(reason, idx) in user.match_reasons"
                :key="idx"
                class="text-xs font-semibold px-3 py-1 rounded-full transition-all duration-300 transform hover:scale-105"
                :style="`
                  background-color: var(--btn-secondary, #facc15);
                  color: var(--btn-primary, #7C0A02);
                `"
              >
                {{ reason }}
              </span>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- Friends List -->
      <div v-if="friendStore.friends.length > 0" class="w-full max-w-6xl mb-16">
        <h2 class="text-2xl font-bold text-gray-700 mb-6">Friends</h2> <!-- ✅ NEW "Friends" Heading -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <RouterLink
            v-for="friend in friendStore.friends"
            :key="friend.id"
            :to="`/profile/${friend.username}`"
            class="flex flex-col items-center p-6 glossy-bg rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group"
          >
            <div v-if="friend.profile_picture">
              <img :src="friend.profile_picture" alt="Profile Picture" class="w-24 h-24 rounded-full object-cover border-4 border-purple-300" />
            </div>
            <div
              v-else
              class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white"
              :style="{ backgroundColor: 'var(--btn-secondary, #facc15)' }"
            >
              {{ friend?.username?.charAt(0)?.toUpperCase() }}
            </div>
            <p class="mt-4 text-lg font-semibold text-gray-800">{{ friend.full_name || friend.username }}</p>
            <p class="text-sm text-gray-600">@{{ friend.username }}</p>

            <button @click.stop.prevent="removeFriend(friend.username)" class="hidden group-hover:block absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white text-xs font-bold py-1 px-2 rounded">
              Remove
            </button>
          </RouterLink>
        </div>
      </div>

      <!-- No Friends -->
      <div v-else-if="!friendStore.loading && friendStore.friends.length === 0" class="text-gray-500 text-lg mt-10">
        You have no friends yet.
      </div>

    </main>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue'
import { useFriendStore } from '@/stores/friend'
import { useToast } from 'vue-toastification'

const toast = useToast()
const friendStore = useFriendStore()

const searchQuery = ref('')
const removingUser = ref(null)

const searchUsers = async () => {
  try {
    await friendStore.searchUsers(searchQuery.value)
  } catch (error) {
    toast.error('Search failed.')
  }
}

const removeFriend = (username) => {
  removingUser.value = username
}

const confirmRemoveFriend = async () => {
  if (!removingUser.value) return
  try {
    await friendStore.removeFriend(removingUser.value)
    toast.success(`${removingUser.value} has been removed.`)
    removingUser.value = null
  } catch (error) {
    toast.error('Failed to remove friend.')
  }
}

onMounted(() => {
  friendStore.fetchFriends()
  friendStore.fetchSuggestions()
})
</script>


