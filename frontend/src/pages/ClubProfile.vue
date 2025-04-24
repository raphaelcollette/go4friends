<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <!-- Loading -->
      <div v-if="loading" class="text-gray-600 text-lg">Loading club...</div>

      <!-- Club Found -->
      <div v-else-if="club && club.name" class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 w-full max-w-4xl text-center">
        <h1 class="text-4xl font-bold text-gray-800 mb-6">{{ club.name }}</h1>
        <p class="text-gray-600 italic mb-10">{{ club.description || 'No description available.' }}</p>

        <h2 class="text-2xl font-bold text-gray-800 mb-6">Members</h2>
        <div v-if="members.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="member in members"
            :key="member.id"
            @click="goToProfile(member.user.username)"
            class="flex flex-col items-center bg-white/30 backdrop-blur-md p-4 rounded-xl hover:bg-white/50 transition-all cursor-pointer"
          >
            <div class="w-20 h-20 rounded-full overflow-hidden flex items-center justify-center bg-purple-200">
              <img v-if="member.user.profile_picture" :src="member.user.profile_picture" alt="Profile" class="w-full h-full object-cover" />
              <div v-else class="text-2xl text-white font-bold">{{ member.user.username?.charAt(0).toUpperCase() }}</div>
            </div>
            <p class="mt-3 font-semibold text-gray-800">
              {{ member.user.username }}
              <span v-if="member.role" class="text-purple-600 text-sm font-bold">({{ member.role }})</span>
            </p>
          </div>
        </div>
        <div v-else class="text-gray-500 text-lg mt-4">No members yet!</div>

        <!-- Admin + Moderator Controls -->
        <div v-if="isStaff" class="mt-8 space-y-4">
          <button class="btn bg-green-600 hover:bg-green-700 w-full" @click="showCreateModal = true">📅 Create Event</button>
          <button class="btn bg-yellow-500 hover:bg-yellow-600 w-full" @click="showManageModal = true">👥 Manage Members</button>

          <!-- Admin Only -->
          <button v-if="isAdmin" class="btn bg-red-600 hover:bg-red-700 w-full" @click="showDeleteModal = true">🗑 Delete Club</button>
        </div>
      </div>

      <!-- Club Not Found -->
      <div v-else class="text-center text-lg text-gray-500 mt-10">❌ Club not found.</div>
    </main>

    <!-- Create Event Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md space-y-4">
        <h2 class="text-xl font-bold text-gray-800 text-center">Create Club Event</h2>
        <input v-model="eventTitle" class="input w-full" placeholder="Event Title" />
        <textarea v-model="eventDescription" class="input w-full" placeholder="Event Description"></textarea>
        <input v-model="eventDate" type="datetime-local" class="input w-full" />
        <input type="file" @change="handleImageUpload" class="input w-full" />
        <div class="flex justify-end space-x-2">
          <button class="btn bg-gray-400 hover:bg-gray-500" @click="showCreateModal = false">Cancel</button>
          <button class="btn bg-green-600 hover:bg-green-700" @click="createEvent">Create</button>
        </div>
      </div>
    </div>

    <!-- Manage Members Modal -->
    <div v-if="showManageModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md space-y-4">
        <h2 class="text-xl font-bold text-center text-gray-800">Manage Members</h2>

        <div v-if="members.length" class="space-y-2 max-h-[300px] overflow-y-auto">
          <div 
            v-for="member in members"
            :key="member.user.username"
            class="flex justify-between items-center border-b pb-2"
          >
            <div>
              <p class="font-medium text-gray-800">{{ member.user.username }}</p>
              <p class="text-sm text-gray-500">Current Role: {{ member.role }}</p>
            </div>

            <div class="flex gap-2 items-center">
              <!-- Role Dropdown -->
              <select
                v-model="roleChanges[member.user.username]"
                @change="updateRole(member.user.username)"
                class="text-sm border rounded px-1 py-0.5"
                :disabled="member.user.username === userStore.currentUser.username"
              >
                <option value="member">member</option>
                <option value="moderator">moderator</option>
                <option value="admin">admin</option>
              </select>

              <!-- Remove Button -->
              <button
                class="text-xs text-red-600 hover:underline"
                @click="removeMember(member.user.username)"
                :disabled="member.user.username === userStore.currentUser.username"
              >
                Remove
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-center text-sm text-gray-500">No members to manage.</div>

        <div class="flex justify-end">
          <button class="btn bg-gray-400 hover:bg-gray-500" @click="showManageModal = false">Close</button>
        </div>
      </div>
    </div>


    <!-- Confirm Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md text-center space-y-4">
        <h2 class="text-xl font-bold text-red-600">Delete Club</h2>
        <p class="text-gray-600">Are you sure you want to permanently delete this club?</p>
        <div class="flex justify-center space-x-4">
          <button class="btn bg-gray-400 hover:bg-gray-500" @click="showDeleteModal = false">Cancel</button>
          <button class="btn bg-red-600 hover:bg-red-700" @click="confirmDeleteClub">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

  
<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useClubStore } from '@/stores/club'
import { useUserStore } from '@/stores/user'
import { authAxios } from '@/utils/axios'
import { useEventStore } from '@/stores/events'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const clubStore = useClubStore()
const userStore = useUserStore()
const eventStore = useEventStore()

const showCreateModal = ref(false)
const showManageModal = ref(false)
const showDeleteModal = ref(false)

const eventTitle = ref('')
const eventDescription = ref('')
const eventDate = ref('')
const eventImage = ref(null)
const roleChanges = ref({})

const clubName = decodeURIComponent(route.params.clubName)

const club = computed(() => clubStore.currentClub)
const members = computed(() => clubStore.clubMembers)
const loading = computed(() => clubStore.loadingClub)

const goToProfile = (username) => router.push(`/profile/${username}`)

watch(members, () => {
  roleChanges.value = {}
  for (const member of members.value) {
    roleChanges.value[member.user.username] = member.role
  }
})


const isAdmin = computed(() => {
  const currentUsername = userStore.currentUser?.username
  const selfMembership = clubStore.clubMembers.find(m => m.user.username === currentUsername)
  return selfMembership?.role === 'admin'
})

const isStaff = computed(() => {
  const currentUsername = userStore.currentUser?.username
  const selfMembership = clubStore.clubMembers.find(m => m.user.username === currentUsername)
  return ['admin', 'moderator'].includes(selfMembership?.role)
})

const handleImageUpload = (e) => {
  eventImage.value = e.target.files[0]
}

const createEvent = async () => {
  if (!eventTitle.value || !eventDate.value) {
    toast.error('Title and date are required')
    return
  }

  const formData = new FormData()
  formData.append('title', eventTitle.value)
  formData.append('description', eventDescription.value)

  const localDate = new Date(eventDate.value)
  formData.append('date', localDate.toISOString()) // ✅ UTC-safe

  formData.append('club_name', club.value.name)

  if (eventImage.value) {
    formData.append('image', eventImage.value)
  }

  try {
    await authAxios.post('/events/create/', formData)
    await eventStore.fetchEvents(true) // force refresh
    toast.success('Event created!')
    showCreateModal.value = false
    eventTitle.value = ''
    eventDescription.value = ''
    eventDate.value = ''
    eventImage.value = null
  } catch (err) {
    console.error('Create event error:', err.response?.data || err.message || err)
    toast.error('Failed to create event.')
  }
}

const confirmDeleteClub = async () => {
  try {
    await authAxios.delete(`/clubs/${encodeURIComponent(club.value.name)}/delete/`)
    toast.success('Club deleted.')
    clubStore.reset()
    router.push('/clubs')
  } catch {
    toast.error('Failed to delete club.')
  }
}


const removeMember = async (username) => {
  try {
    await authAxios.post(`/clubs/${encodeURIComponent(club.value.name)}/remove-member/`, {
      username,
    })
    toast.success(`${username} removed from club`)
    await clubStore.fetchClubProfile(clubName)
  } catch {
    toast.error('Failed to remove member.')
  }
}


const updateRole = async (username) => {
  const newRole = roleChanges.value[username]
  try {
    await authAxios.post(`/clubs/${encodeURIComponent(club.value.name)}/update-role/`, {
      username,
      role: newRole,
    })
    toast.success(`${username}'s role updated to ${newRole}`)
    await clubStore.fetchClubProfile(clubName)
  } catch {
    toast.error('Failed to update role.')
  }
}


onMounted(async () => {
  try {
    await clubStore.fetchClubProfile(clubName)
  } catch {
    toast.error('Could not load club.')
  }
})
</script>
  
<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
.input {
  @apply w-full bg-white border border-gray-300 rounded-xl p-3 text-base focus:outline-none focus:ring-2 focus:ring-purple-400;
}
</style>
  
  
  