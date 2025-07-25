<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <!-- Loading -->
      <div v-if="loading" class="text-gray-600 text-lg">Loading club...</div>

      <!-- Club Found -->
      <div v-else-if="club && club.name" class="glossy-bg rounded-2xl shadow-lg p-8 w-full max-w-4xl text-center">
        <h1 class="text-4xl font-bold text-gray-800 mb-6">{{ club.name }}</h1>
        <p class="text-gray-600 italic mb-10">{{ club.description || 'No description available.' }}</p>

        <h2 class="text-2xl font-bold text-gray-800 mb-6">Members</h2>
        <div v-if="members.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="member in members"
            :key="member.id"
            @click="goToProfile(member.user.username)"
            class="flex flex-col items-center glossy-bg p-4 rounded-xl hover:brightness-105 transition-all cursor-pointer"
          >
            <div class="w-20 h-20 rounded-full overflow-hidden flex items-center justify-center bg-purple-200">
              <img v-if="member.user.profile_picture_url" :src="member.user.profile_picture_url" alt="Profile" class="w-full h-full object-cover" />
              <div
                v-else
                class="w-full h-full flex items-center justify-center text-white text-2xl font-bold"
                :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
              >
                {{ member.user.username?.charAt(0).toUpperCase() }}
              </div>
            </div>
            <p class="mt-3 font-semibold text-gray-800">
              {{ member.user.username }}
              <span v-if="member.role" class="text-purple-600 text-sm font-bold">({{ member.role }})</span>
            </p>
          </div>
        </div>
        <div v-else class="text-gray-500 text-lg mt-4">No members yet!</div>

        <div v-if="isMember" class="mt-8 space-y-4">
          <button class="btn w-full" @click="openClubMessages">💬 Message Group</button>
        </div>
        <!-- Admin + Moderator Controls -->
        <div v-if="isStaff" class="mt-8 space-y-4">
          <button class="btn w-full" @click="showCreateModal = true">📅 Create Event</button>
          <button class="btn w-full" @click="showManageModal = true">👥 Manage Members</button>
        
          <!-- Admin Only -->
          <button v-if="isAdmin" class="redbtn w-full" @click="showDeleteModal = true">🗑 Delete Club</button>
        </div>

        <button
          v-if="club?.is_private && isStaff"
          class="btn w-full mt-4"
          @click="showInviteModal = true"
        >
          ✉️ Invite User
        </button>
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
        <input v-model="eventLocation" class="input w-full" placeholder="Event Location" />
        <input v-model="eventDate" type="datetime-local" class="input w-full" />
        <input type="file" @change="handleImageUpload" class="input w-full" />
        <div class="flex justify-end space-x-2">
          <button class="btn" @click="showCreateModal = false">Cancel</button>
          <button class="btn" @click="createEvent">Create</button>
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
          <button class="btn" @click="showManageModal = false">Close</button>
        </div>
      </div>
    </div>

    <!-- Invite User Modal -->
    <div v-if="showInviteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md space-y-4">
        <h2 class="text-xl font-bold text-gray-800 text-center">Invite User to Club</h2>
        <input v-model="inviteUsername" class="input w-full" placeholder="Enter username to invite" />
        <div class="flex justify-end space-x-2">
          <button class="btn" @click="showInviteModal = false">Cancel</button>
          <button class="btn" @click="sendInvite">Send Invite</button>
        </div>
      </div>
    </div>

    <!-- Confirm Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md text-center space-y-4">
        <h2 class="text-xl font-bold text-red-600">Delete Club</h2>
        <p class="text-gray-600">Are you sure you want to permanently delete this club?</p>
        <div class="flex justify-center space-x-4">
          <button class="btn" @click="showDeleteModal = false">Cancel</button>
          <button class="redbtn" @click="confirmDeleteClub">Delete</button>
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
const showInviteModal = ref(false)
const inviteUsername = ref('')
const eventLocation = ref('')

const clubName = decodeURIComponent(route.params.clubName)

const club = computed(() => clubStore.currentClub)
const members = computed(() => clubStore.clubMembers)
const loading = computed(() => clubStore.loadingClub)

const threads = ref([]) // fetched from API
const clubThreadId = computed(() => {
  const match = threads.value.find(
    t => t.club_name === club.value.name && t.is_group
  )
  return match?.id || null
})

const goToProfile = (username) => router.push(`/profile/${username}`)

watch(members, () => {
  roleChanges.value = {}
  for (const member of members.value) {
    roleChanges.value[member.user.username] = member.role
  }
})

const isMember = computed(() => {
  const username = userStore.currentUser?.username
  return clubStore.clubMembers.some(m => m.user.username === username)
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
  formData.append('location', eventLocation.value)
  const localDate = new Date(eventDate.value)
  formData.append('date', localDate.toISOString())

  formData.append('club_name', club.value.name)

  if (eventImage.value) {
    formData.append('image', eventImage.value)
  }

  try {
    await authAxios.post('/events/create/', formData)
    await eventStore.fetchEvents(true)        
    await clubStore.fetchMyClubs(true)           
    toast.success('Event created!')
    showCreateModal.value = false
    eventTitle.value = ''
    eventDescription.value = ''
    eventDate.value = ''
    eventLocation.value = ''
    eventImage.value = null
  } catch (err) {
    console.error('Create event error:', err.response?.data || err.message || err)

    const data = err?.response?.data
    const titleError = data?.title?.[0]
    const descriptionError = data?.description?.[0]
    const locationError = data?.location?.[0]

    if (titleError?.includes('inappropriate')) {
      toast.error('Event title contains inappropriate language.')
    } else if (descriptionError?.includes('inappropriate')) {
      toast.error('Event description contains inappropriate language.')
    } else if (locationError?.includes('inappropriate')) {
      toast.error('Event location contains inappropriate language.')
    } else if (titleError) {
      toast.error(titleError)
    } else if (descriptionError) {
      toast.error(descriptionError)
    } else if (locationError) {
      toast.error(locationError)
    } else {
      toast.error('Failed to create event.')
    }
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

const sendInvite = async () => {
  if (!inviteUsername.value.trim()) {
    toast.error('Please enter a username to invite.')
    return
  }

  try {
    await authAxios.post(`/clubs/${encodeURIComponent(club.value.name)}/invite/`, {
      username: inviteUsername.value.trim(),
    })
    toast.success('Invite sent!')
    showInviteModal.value = false
    inviteUsername.value = ''
  } catch (err) {
    console.error(err)
    toast.error(err.response?.data?.error || 'Failed to send invite.')
  }
}


const openClubMessages = () => {
  router.push(`/messages?thread=${clubThreadId.value}`)
}


onMounted(async () => {
  try {
    await Promise.all([
      clubStore.fetchClubProfile(clubName),
      (async () => {
        const res = await authAxios.get('/messages/threads/')
        threads.value = res.data
      })()
    ])
  } catch {
    toast.error('Could not load club or threads.')
  }
})
</script>
  
<style scoped>

</style>
  
  
  