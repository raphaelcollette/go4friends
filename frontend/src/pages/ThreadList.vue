<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6 w-full">
      <div class="w-full max-w-2xl bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 space-y-4">
        <h2 class="text-3xl font-bold text-gray-800 mb-4">Messages</h2>

        <div v-if="sortedThreads.length > 0" class="space-y-4">
          <div
            v-for="thread in sortedThreads"
            :key="thread.id"
            @click="goToThread(thread.id)"
            class="p-4 rounded-xl bg-white/60 backdrop-blur hover:bg-white/80 cursor-pointer shadow transition"
          >
          <div class="font-semibold text-lg text-gray-800">
            <span v-if="thread.club_name">{{ thread.club_name }} (Club Chat)</span>
            <span v-else>{{ getOtherUsernames(thread.participants) }}</span>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'
import { useFriendStore } from '@/stores/friend'
import { useMessageStore } from '@/stores/messages'

const router = useRouter()
const toast = useToast()

const userStore = useUserStore()
const friendStore = useFriendStore()
const messageStore = useMessageStore()

const showModal = ref(false)
const selectedUsers = ref([])

const sortedThreads = computed(() => {
  return [...messageStore.threads].sort((a, b) => {
    const t1 = new Date(a.last_message?.timestamp || 0).getTime()
    const t2 = new Date(b.last_message?.timestamp || 0).getTime()
    return t2 - t1
  })
})

const friends = computed(() => friendStore.friends)

const formatTime = (timestamp) => {
  return timestamp ? new Date(timestamp).toLocaleString() : ''
}

const goToThread = (id) => {
  router.push(`/messages/thread/${id}`)
}

const getOtherUsernames = (participants) => {
  return participants
    .filter(p => p.user && p.user.username !== userStore.currentUser?.username)
    .map(p => p.user.username)
    .join(', ')
}

const createGroupChat = async () => {
  if (selectedUsers.value.length < 2) {
    toast.error('Select at least 2 users to create a group chat.')
    return
  }

  try {
    const res = await messageStore.startGroupThread(selectedUsers.value)
    toast.success('Group chat created!')
    showModal.value = false
    selectedUsers.value = []
    router.push(`/messages/thread/${res.thread_id}`)
  } catch {
    toast.error('Failed to create group chat.')
  }
}

onMounted(async () => {
  await userStore.fetchCurrentUser()
  await friendStore.fetchFriends()
  await messageStore.fetchThreads()
})
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300;
}
</style>
