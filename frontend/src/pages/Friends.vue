<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col sm:flex-row items-start pt-24 px-6 gap-8">

      <!-- Left: Main Content -->
      <div class="flex-1 w-full max-w-6xl mx-auto">
        <!-- Header -->
        <div class="flex justify-between items-center mb-10">
          <h1 class="text-4xl font-extrabold text-gray-800">Your Friends</h1>
          <div class="flex space-x-4">
            <input v-model="searchQuery" type="text" placeholder="Search users..." class="input" />
            <button class="btn" @click="searchUsers">Search</button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="friendStore.loading" class="text-gray-600 text-lg">Loading friends...</div>

        <!-- Search Results -->
        <div v-else-if="friendStore.searchResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 mb-16">
          <RouterLink
            v-for="user in friendStore.searchResults"
            :key="user.id"
            :to="`/profile/${user.username}`"
            class="flex flex-col items-center p-6 glossy-bg rounded-2xl shadow-md hover:shadow-xl transform hover:scale-105 transition-all duration-300 no-underline relative group cursor-pointer"
          >
            <div v-if="user.profile_picture_url">
              <img :src="user.profile_picture_url" alt="Profile Picture" class="w-24 h-24 rounded-full object-cover border-4" :style="{ borderColor: 'var(--btn-primary, #7A0019)' }" />
            </div>
            <div v-else class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white" :style="{ backgroundColor: 'var(--btn-primary, #7A0019)' }">
              {{ user?.username?.charAt(0)?.toUpperCase() }}
            </div>
            <p class="mt-4 text-lg font-semibold text-gray-800">{{ user.full_name || user.username }}</p>
            <p class="text-sm text-gray-600">@{{ user.username }}</p>
          </RouterLink>
        </div>

        <!-- Friends List -->
        <div v-if="friendStore.friends.length > 0" class="mb-16">
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
              <div v-else class="w-24 h-24 rounded-full flex items-center justify-center text-3xl text-white" :style="{ backgroundColor: 'var(--btn-primary, #7A0019)' }">
                {{ friend?.username?.charAt(0)?.toUpperCase() }}
              </div>
              <p class="mt-4 text-lg font-semibold text-gray-800">{{ friend.full_name || friend.username }}</p>
              <p class="text-sm text-gray-600">@{{ friend.username }}</p>

              <button @click.stop.prevent="friendStore.removeFriend(friend.username)" class="hidden group-hover:block absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white text-xs font-bold py-1 px-2 rounded">
                Remove
              </button>
            </RouterLink>
          </div>
        </div>

        <!-- No Friends -->
        <div v-else-if="!friendStore.loading && friendStore.friends.length === 0" class="text-gray-500 text-lg mt-10 text-center">
          You have no friends yet.
        </div>
      </div>

      <!-- Right: Sidebar -->
      <div class="flex flex-col w-full sm:w-96 gap-6">
        <!-- Suggested Friends -->
        <div class="glossy-bg rounded-2xl p-6 shadow-md">
          <h2 class="text-2xl font-bold text-gray-700 mb-4">Suggested Friends</h2>
          <div v-if="friendStore.suggested.length > 0" class="space-y-4">
            <RouterLink
              v-for="user in friendStore.suggested"
              :key="user.id"
              :to="`/profile/${user.username}`"
              class="flex items-center gap-3 glossy-bg p-3 rounded-xl hover:brightness-105 transition cursor-pointer"
            >
              <div v-if="user.profile_picture_url">
                <img :src="user.profile_picture_url" alt="Profile" class="w-12 h-12 rounded-full object-cover border-2" :style="{ borderColor: 'var(--btn-primary, #7A0019)' }" />
              </div>
              <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg text-white" :style="{ backgroundColor: 'var(--btn-primary, #7A0019)' }">
                {{ user?.username?.charAt(0)?.toUpperCase() }}
              </div>
              <div class="flex-1">
                <p class="font-semibold text-gray-800">{{ user.full_name || user.username }}</p>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span
                    v-for="(reason, idx) in user.match_reasons"
                    :key="idx"
                    class="text-xs font-semibold px-2 py-1 rounded-full"
                    :style="`
                      background-color: var(--btn-secondary, #FFCC33);
                      color: var(--btn-primary, #7A0019);
                    `"
                  >
                    {{ reason }}
                  </span>
                </div>
              </div>
            </RouterLink>
          </div>
          <div v-else class="text-gray-500 text-sm">No suggestions yet.</div>
        </div>

        <!-- Friend Requests -->
        <div class="glossy-bg rounded-2xl p-6 shadow-md">
          <h2 class="text-2xl font-bold text-gray-700 mb-4">Friend Requests</h2>
          <div v-if="friendStore.pendingRequests.length > 0" class="space-y-4">
            <div
              v-for="request in friendStore.pendingRequests"
              :key="request.id"
              class="flex items-center justify-between glossy-bg p-3 rounded-xl hover:brightness-105 transition"
            >
              <RouterLink :to="`/profile/${request.from_username}`" class="flex items-center gap-3">
                <div v-if="request.from_profile_picture">
                  <img :src="request.from_profile_picture" alt="Profile" class="w-12 h-12 rounded-full object-cover border-2" :style="{ borderColor: 'var(--btn-primary, #7A0019)' }" />
                </div>
                <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg text-white" :style="{ backgroundColor: 'var(--btn-primary, #7A0019)' }">
                  {{ request?.from_username?.charAt(0)?.toUpperCase() }}
                </div>
                <p class="font-semibold text-gray-800">{{ request.from_username }}</p>
              </RouterLink>

              <div class="flex gap-2">
                <button class="greenbtn text-xs" @click="friendStore.acceptRequest(request.from_username)">Accept</button>
                <button class="redbtn text-xs" @click="friendStore.rejectRequest(request.from_username)">Reject</button>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">No requests yet.</div>
        </div>
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

const searchUsers = async () => {
  try {
    await friendStore.searchUsers(searchQuery.value)
  } catch (error) {
    toast.error('Search failed.')
  }
}


onMounted(() => {
  friendStore.fetchFriends()
  friendStore.fetchSuggestions()
})
</script>


