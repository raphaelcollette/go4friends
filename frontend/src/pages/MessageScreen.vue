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
        <div ref="messageContainer" class="flex-1 flex flex-col space-y-4 overflow-y-auto">

          <div v-if="activeThreadId && groupedMessages.length > 0">
            <div
              v-for="(group, index) in groupedMessages"
              :key="index"
              class="flex flex-col mb-6"
              :class="group.sender.username === currentUser.username ? 'items-end' : 'items-start'"
            >
              <div v-if="index === 0 || groupedMessages[index - 1].sender.username !== group.sender.username"
                class="text-xs font-semibold text-gray-700 mb-1">
                {{ group.sender.full_name || group.sender.username }}
              </div>

              <!-- Messages in the group -->
              <div class="flex flex-col space-y-1">
                <div
                  v-for="(text, idx) in group.messages"
                  :key="idx"
                  class="px-4 py-2 rounded-xl text-white break-words max-w-xs w-fit"
                  :class="[
                    group.sender.username === currentUser.username ? 'self-end bg-primary' : 'self-start bg-gray-600'
                  ]"
                >
                  {{ text }}
                </div>
              </div>

              <div class="text-xs text-gray-400 mt-1">
                {{ formatTime(group.lastTimestamp) }}
              </div>
            </div>
          </div>

          <!-- No thread selected -->
          <div v-else class="flex-1 flex items-center justify-center text-gray-400">
            Select a chat to start messaging
          </div>

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

const groupedMessages = computed(() => {
  const groups = []
  let currentGroup = null

  const FIVE_MINUTES = 5 * 60 * 1000 // ms

  for (const msg of messageStore.messagesByThread[activeThreadId.value] || []) {
    if (
      !currentGroup ||
      currentGroup.sender.username !== msg.sender.username ||
      new Date(msg.timestamp) - new Date(currentGroup.lastTimestamp) > FIVE_MINUTES
    ) {
      // Start a new group
      if (currentGroup) groups.push(currentGroup)

      currentGroup = {
        sender: msg.sender,
        messages: [msg.message],
        lastTimestamp: msg.timestamp
      }
    } else {
      // Add to current group
      currentGroup.messages.push(msg.message)
      currentGroup.lastTimestamp = msg.timestamp
    }
  }

  if (currentGroup) groups.push(currentGroup)

  return groups
})

watch(() => groupedMessages.value.length, async () => {
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
