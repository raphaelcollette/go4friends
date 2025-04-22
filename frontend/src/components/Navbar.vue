<template>
  <nav class="w-full p-4 flex justify-between items-center bg-white/30 backdrop-blur-md shadow-md fixed top-0 z-50">
    <RouterLink to="/main" class="text-2xl font-bold text-purple-700">
      whatsurmajor
    </RouterLink>

    <div class="flex space-x-4">
      <RouterLink to="/clubs" class="btn">Clubs</RouterLink>
      <RouterLink to="/events" class="btn">Events</RouterLink>
      <RouterLink to="/friends" class="btn">Friends</RouterLink>
      <RouterLink
        v-if="currentUser"
        :to="`/profile/${currentUser.username}`"
        class="btn"
      >
        Profile
      </RouterLink>
      <RouterLink to="/settings" class="btn">Settings</RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authAxios } from '@/utils/axios'

const currentUser = ref(null)

const fetchCurrentUser = async () => {
  try {
    const res = await authAxios.get('/users/me/')
    currentUser.value = res.data
  } catch (error) {
    console.error('Failed to fetch current user:', error)
  }
}

onMounted(fetchCurrentUser)
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-xl text-base transition-all duration-300;
}
</style>