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
                    <!-- Group Chat Button -->
            <div class="mt-6 w-full max-w-2xl">
            <button @click="showModal = true" class="btn w-full">+ New Group Chat</button>
            </div>

            <!-- Modal -->
            <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div class="bg-white rounded-2xl shadow-lg p-6 w-full max-w-md space-y-4">
                <h2 class="text-xl font-bold text-gray-800">Create Group Chat</h2>

                <div v-if="friends.length">
                <p class="text-gray-600 text-sm mb-2">Select friends to add:</p>
                <div class="max-h-40 overflow-y-auto space-y-2">
                    <div v-for="friend in friends" :key="friend.username" class="flex items-center space-x-2">
                    <input type="checkbox" :value="friend.username" v-model="selectedUsers" class="form-checkbox text-purple-600">
                    <span>{{ friend.full_name || friend.username }}</span>
                    </div>
                </div>
                </div>
                <div v-else class="text-gray-500 text-sm">You have no friends to add.</div>

                <div class="flex justify-end space-x-2">
                <button @click="createGroupChat" class="btn bg-green-600 hover:bg-green-700">Create</button>
                <button @click="showModal = false" class="btn bg-gray-400 hover:bg-gray-500">Cancel</button>
                </div>
            </div>
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
  const showModal = ref(false)
  const friends = ref([])
  const selectedUsers = ref([])
  
  const fetchThreads = async () => {
  try {
    const res = await authAxios.get('/messages/threads/')
    threads.value = res.data
      .slice()
      .sort((a, b) => {
        const timeA = a.last_message?.timestamp ? new Date(a.last_message.timestamp).getTime() : 0
        const timeB = b.last_message?.timestamp ? new Date(b.last_message.timestamp).getTime() : 0
        return timeB - timeA // descending
      })
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

  const fetchFriends = async () => {
  try {
    const res = await authAxios.get('/friends/friends/')
    friends.value = res.data
  } catch {
    toast.error('Failed to load friends.')
  }
}

const createGroupChat = async () => {
  if (selectedUsers.value.length < 2) {
    toast.error('Select at least 2 users to create a group chat.')
    return
  }

  try {
    const res = await authAxios.post('/messages/threads/start-private/', {
      usernames: selectedUsers.value
    })
    toast.success('Group chat created!')
    showModal.value = false
    selectedUsers.value = []
    await fetchThreads()
    router.push(`/messages/thread/${res.data.thread_id}`)
  } catch (err) {
    toast.error('Failed to create group chat.')
  }
}
  
  onMounted(async () => {
    await fetchCurrentUser()
    await fetchThreads()
    await fetchFriends()
  })
  </script>
  
  <style scoped>
  </style>