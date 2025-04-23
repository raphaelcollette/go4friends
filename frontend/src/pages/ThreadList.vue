<template>
    <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
      <Navbar />
  
      <main class="flex-1 flex flex-col items-center pt-24 px-6 w-full">
        <div class="w-full max-w-2xl bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 space-y-4">
          <h2 class="text-3xl font-bold text-gray-800 mb-4">Messages</h2>
  
          <!-- Threads List -->
          <div v-if="threads.length > 0" class="space-y-4">
            <div
              v-for="thread in threads"
              :key="thread.id"
              @click="goToThread(thread.id)"
              class="p-4 rounded-xl bg-white/60 backdrop-blur hover:bg-white/80 cursor-pointer shadow transition"
            >
              <div class="font-semibold text-lg text-gray-800">
                {{ getOtherUsernames(thread.participants) }}
              </div>
              <div class="text-sm text-gray-600 mt-1">
                {{ thread.last_message?.message || 'No messages yet' }}
              </div>
              <div class="text-xs text-gray-400 mt-1">
                {{ formatTime(thread.last_message?.timestamp) }}
              </div>
            </div>
          </div>
  
          <div v-else class="text-gray-600 text-center">No recent conversations yet.</div>
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { authAxios } from '@/utils/axios'
  import Navbar from '@/components/Navbar.vue'
  import { useToast } from 'vue-toastification'
  
  const router = useRouter()
  const toast = useToast()
  const threads = ref([])
  const currentUser = ref({})
  
  const fetchThreads = async () => {
    try {
      const res = await authAxios.get('/messages/threads/')
      threads.value = res.data
    } catch (err) {
      toast.error('Failed to load threads.')
    }
  }
  
  const fetchCurrentUser = async () => {
    try {
      const res = await authAxios.get('/users/me/')
      currentUser.value = res.data
    } catch {
      toast.error('Failed to load current user.')
    }
  }
  
  const getOtherUsernames = (participants) => {
  return participants
    .filter(p => p.user && p.user.username !== currentUser.value.username)
    .map(p => p.user.username)
    .join(', ')
}
  
  const formatTime = (timestamp) => {
    return timestamp ? new Date(timestamp).toLocaleString() : ''
  }
  
  const goToThread = (id) => {
    router.push(`/messages/thread/${id}`)
  }
  
  onMounted(async () => {
    await fetchCurrentUser()
    await fetchThreads()
  })
  </script>
  
  <style scoped>
  </style>