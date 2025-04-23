<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

    <main class="flex-1 flex flex-col items-center pt-24 px-6 w-full">
      <div class="w-full max-w-2xl bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 space-y-4">
        <h2 class="text-2xl font-bold text-gray-800">Chat</h2>

        <!-- Messages -->
        <div class="flex flex-col space-y-2 max-h-[400px] overflow-y-auto">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="msg.sender.username === currentUser.username ? 'self-end text-right' : 'self-start text-left'"
          >
            <div class="inline-block px-4 py-2 rounded-xl text-white"
              :class="msg.sender.username === currentUser.username ? 'bg-purple-600' : 'bg-gray-500'">
              {{ msg.message }}
            </div>
            <div class="text-xs text-gray-600 mt-1">
              {{ formatTime(msg.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Send Message -->
        <form @submit.prevent="sendMessage" class="flex mt-4 space-x-2">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type your message..."
            class="input flex-1"
          />
          <button type="submit" class="btn">Send</button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

const route = useRoute()
const toast = useToast()
const threadId = route.params.threadId

const currentUser = ref({})
const messages = ref([])
const newMessage = ref('')

const fetchCurrentUser = async () => {
  try {
    const res = await authAxios.get('/users/me/')
    currentUser.value = res.data
  } catch {
    toast.error('Failed to load current user.')
  }
}

const fetchMessages = async () => {
  try {
    const res = await authAxios.get(`/messages/threads/${threadId}/messages/`)
    messages.value = res.data.reverse()
  } catch (error) {
    toast.error('Failed to load messages.')
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return

  try {
    await authAxios.post(`/messages/threads/${threadId}/send/`, {
      message: newMessage.value.trim(),
    })
    newMessage.value = ''
    fetchMessages()
  } catch (error) {
    toast.error('Failed to send message.')
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(async () => {
  await fetchCurrentUser()
  await fetchMessages()
})
</script>

<style scoped>
.input {
  @apply p-3 rounded-xl bg-white/60 backdrop-blur-sm placeholder-gray-500 text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-400;
}
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300;
}
</style>
