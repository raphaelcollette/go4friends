<template>
    <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden pt-24 pb-12">
      <div class="flex flex-1 w-full max-w-6xl mx-auto bg-white/20 backdrop-blur-md rounded-2xl shadow-md overflow-hidden">
        <!-- Left: Threads -->
        <div class="w-1/3 border-r p-4 overflow-y-auto">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Chats</h2>
  
          <div v-if="sortedThreads.length > 0" class="space-y-2">
            <div
              v-for="thread in sortedThreads"
              :key="thread.id"
              @click="selectThread(thread.id)"
              :class="['p-3 rounded-xl cursor-pointer transition', thread.id === activeThreadId ? 'bg-white/70' : 'hover:bg-white/50']"
            >
              <div class="font-semibold">
                <span v-if="thread.club_name">{{ thread.club_name }}</span>
                <span v-else>{{ getOtherUsernames(thread.participants) }}</span>
              </div>
              <div class="text-xs text-gray-600 truncate">{{ thread.last_message?.message || 'No messages yet' }}</div>
            </div>
          </div>
          <div v-else class="text-gray-500 text-center">No conversations yet.</div>
  
          <!-- New Group Button -->
          <div class="mt-6">
            <button @click="showModal = true" class="btn w-full">+ New Group</button>
          </div>
        </div>
  
        <!-- Right: Messages -->
        <div class="flex-1 flex flex-col p-6">
          <div v-if="activeThreadId && currentMessages.length > 0" class="flex-1 flex flex-col space-y-4 overflow-y-auto" ref="messageContainer">
            <div
              v-for="(msg, index) in currentMessages"
              :key="msg.id"
              :class="msg.sender.username === currentUser.username ? 'self-end text-right' : 'self-start text-left'"
            >
              <div
                v-if="index === 0 || currentMessages[index - 1].sender.username !== msg.sender.username"
                class="text-xs font-semibold text-gray-700 mb-1"
              >
                {{ msg.sender.full_name || msg.sender.username }}
              </div>
  
              <div
                class="inline-block px-4 py-2 rounded-xl text-white max-w-xs break-words"
                :style="msg.sender.username === currentUser.username
                  ? 'background-color: var(--btn-primary, #6366f1);'
                  : 'background-color: #6b7280;'"
              >
                {{ msg.message }}
              </div>
              <div class="text-xs text-gray-400 mt-1">{{ formatTime(msg.timestamp) }}</div>
            </div>
          </div>
  
          <!-- If no thread selected -->
          <div v-else class="flex-1 flex items-center justify-center text-gray-400">
            Select a chat to start messaging
          </div>
  
          <!-- Send Message Box -->
          <form v-if="activeThreadId" @submit.prevent="sendMessage" class="flex space-x-2 mt-4">
            <input v-model="newMessage" type="text" placeholder="Type a message..." class="input flex-1" />
            <button type="submit" class="btn">Send</button>
          </form>
        </div>
      </div>
  
      <!-- Create Group Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white rounded-2xl shadow-lg p-6 w-full max-w-md">
          <h2 class="text-xl font-bold mb-4">Create Group Chat</h2>
  
          <div v-if="friends.length">
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <div v-for="friend in friends" :key="friend.username" class="flex items-center space-x-2">
                <input type="checkbox" :value="friend.username" v-model="selectedUsers" />
                <span>{{ friend.full_name || friend.username }}</span>
              </div>
            </div>
          </div>
          <div v-else class="text-gray-400">No friends to add.</div>
  
          <div class="flex justify-end space-x-2 mt-4">
            <button class="btn bg-green-500" @click="createGroupChat">Create</button>
            <button class="btn bg-gray-400" @click="showModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  



<script setup>
import { ref, computed, onMounted, nextTick, watch, onUnmounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'
import { useFriendStore } from '@/stores/friend'
import { useMessageStore } from '@/stores/messages'

const toast = useToast()
const userStore = useUserStore()
const friendStore = useFriendStore()
const messageStore = useMessageStore()

const showModal = ref(false)
const selectedUsers = ref([])
const activeThreadId = ref(null)
const newMessage = ref('')
const messageContainer = ref(null)

const currentUser = computed(() => userStore.currentUser)
const sortedThreads = computed(() => {
  return [...messageStore.threads].sort((a, b) => {
    const t1 = new Date(a.last_message?.timestamp || 0).getTime()
    const t2 = new Date(b.last_message?.timestamp || 0).getTime()
    return t2 - t1
  })
})
const friends = computed(() => friendStore.friends)

const currentMessages = computed(() => {
  return messageStore.messagesByThread[activeThreadId.value] || []
})

watch(() => currentMessages.value.length, async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
})

const formatTime = (timestamp) => timestamp ? new Date(timestamp).toLocaleString() : ''

const selectThread = async (id) => {
  activeThreadId.value = id
  if (!messageStore.messagesByThread[id]) {
    await messageStore.fetchMessages(id, true)
  }
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeThreadId.value) return
  try {
    await messageStore.sendMessage(activeThreadId.value, newMessage.value.trim())
    newMessage.value = ''
    await nextTick()
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
    await messageStore.fetchThreads(true) // Refresh threads
  } catch {
    toast.error('Failed to send message')
  }
}

const getOtherUsernames = (participants) => {
  return participants
    .filter(p => p.user && p.user.username !== userStore.currentUser?.username)
    .map(p => p.user.username)
    .join(', ')
}

const createGroupChat = async () => {
  if (selectedUsers.value.length < 2) {
    toast.error('Select at least 2 friends')
    return
  }
  try {
    const res = await messageStore.startGroupThread(selectedUsers.value)
    toast.success('Group chat created!')
    showModal.value = false
    selectedUsers.value = []
    activeThreadId.value = res.thread_id
    await messageStore.fetchThreads(true)
    await selectThread(res.thread_id)
  } catch {
    toast.error('Failed to create group')
  }
}

let pollingInterval = null

onMounted(async () => {
  await userStore.fetchCurrentUser()
  await friendStore.fetchFriends()
  await messageStore.fetchThreads()

  pollingInterval = setInterval(async () => {
    await messageStore.fetchThreads(true) // force refresh threads every 15 seconds
  }, 15000) // 15000ms = 15 seconds

})

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval) // ✅ clean up
  }
})
</script>
