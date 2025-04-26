<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col items-center pt-24 px-6 relative">
      
      <!-- Main Layout with sidebar -->
      <div class="flex w-full max-w-7xl space-x-6">
        
        <!-- Main Content (Clubs) -->
        <div class="flex-1">
          <!-- Header -->
          <div class="flex justify-between items-center mb-10">
            <h1 class="text-4xl font-extrabold text-gray-800">Clubs</h1>
            <button class="btn" @click="showCreate = true">+ Create Club</button>
          </div>

          <!-- Create Club Modal -->
          <div v-if="showCreate" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div class="bg-white rounded-2xl p-8 w-full max-w-md space-y-6">
              <h2 class="text-2xl font-bold text-center">Create a New Club</h2>

              <input v-model="newClubName" type="text" placeholder="Club Name" class="input w-full" />
              <textarea v-model="newClubDescription" placeholder="Club Description" class="input w-full"></textarea>

              <label class="flex items-center space-x-2 mt-2">
                <input type="checkbox" v-model="newClubPrivate" class="form-checkbox h-5 w-5 text-purple-600" />
                <span class="text-gray-700 font-medium">Private Club (invite-only)</span>
              </label>

              <div class="flex justify-end space-x-4 mt-4">
                <button class="btn" @click="resetCreateModal">Cancel</button>
                <button class="greenbtn" @click="createClub">Create</button>
              </div>
            </div>
          </div>

          <!-- Clubs List -->
          <div v-if="clubs.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">
            <div
              v-for="club in clubs"
              :key="club.id"
              @click="club.name && goToClub(club.name)"
              class="glossy-bg rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300 cursor-pointer"
            >
              <span
                v-if="club.is_private"
                class="mt-2 inline-block px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded-full"
              >
                Private
              </span>

              <h3 class="text-2xl font-bold text-gray-800 mt-2">{{ club.name }}</h3>
              <p class="text-gray-600 mt-2">{{ club.description || 'No description provided.' }}</p>

              <div class="mt-4">
                <button v-if="!club.is_private && !club.is_member" class="greenbtn" @click.stop="joinClub(club.name)">Join</button>
                <button v-else-if="club.is_member && club.only_member_is_me" class="redbtn" @click.stop="requestDeleteClub(club.name)">Delete</button>
                <button v-else-if="club.is_member" class="redbtn" @click.stop="leaveClub(club.name)">Leave</button>
                <span v-else-if="club.is_private && !club.is_member" class="inline-block px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded-full">
                  Invite Only
                </span>
              </div>
            </div>
          </div>

          <!-- No Clubs Message -->
          <div v-else class="text-gray-500 text-lg mt-10">
            No clubs yet. Be the first to create one!
          </div>

          <!-- Pending Invites Section -->
          <div v-if="invites.length > 0" class="mt-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-6">📨 Your Club Invites</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
              <div
                v-for="invite in invites"
                :key="invite.id"
                class="glossy-bg rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300"
              >
                <h3 class="text-2xl font-bold text-gray-800">{{ invite.club }}</h3>
                <p class="text-sm text-gray-600 mt-1">Invited by: <span class="font-semibold text-purple-700">{{ invite.invited_by }}</span></p>
                <div class="flex gap-2 mt-6">
                  <button class="greenbtn" @click="acceptInvite(invite.id)">Accept</button>
                  <button class="redbtn" @click="rejectInvite(invite.id)">Reject</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Sidebar (Suggested Clubs) -->
        <div class="w-72 hidden lg:block">
          <div class="glossy-bg p-6 rounded-2xl shadow-md space-y-4 sticky top-32">
            <h2 class="text-xl font-bold text-gray-800 mb-4">🔥 Suggested Clubs</h2>

            <div class="space-y-3">
              <div class="bg-white/30 backdrop-blur rounded-lg p-3 hover:brightness-110 transition">
                <p class="font-semibold text-gray-700">Coding Club</p>
                <p class="text-xs text-gray-500">Learn and hack together!</p>
              </div>
              <div class="bg-white/30 backdrop-blur rounded-lg p-3 hover:brightness-110 transition">
                <p class="font-semibold text-gray-700">Chess Society</p>
                <p class="text-xs text-gray-500">Challenge and compete weekly.</p>
              </div>
              <div class="bg-white/30 backdrop-blur rounded-lg p-3 hover:brightness-110 transition">
                <p class="font-semibold text-gray-700">Photography Club</p>
                <p class="text-xs text-gray-500">Capture your best moments!</p>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Delete Club Confirmation Modal -->
      <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md text-center space-y-4">
          <h2 class="text-xl font-bold text-red-600">Delete Club</h2>
          <p class="text-gray-600">Are you sure you want to permanently delete <strong>{{ clubToDelete }}</strong>?</p>
          <div class="flex justify-center space-x-4">
            <button class="btn" @click="showDeleteConfirm = false">Cancel</button>
            <button class="redbtn" @click="confirmDeleteClub">Delete</button>
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
import { useClubStore } from '@/stores/club'
import { useInviteStore } from '@/stores/invites'
import { authAxios } from '@/utils/axios'
import { useMessageStore } from '@/stores/messages'

const toast = useToast()
const router = useRouter()
const clubStore = useClubStore()
const inviteStore = useInviteStore()
const messageStore = useMessageStore()
const invites = computed(() => inviteStore.invites)

const showCreate = ref(false)
const newClubName = ref('')
const newClubDescription = ref('')
const newClubPrivate = ref(false)
const showDeleteConfirm = ref(false)
const clubToDelete = ref(null)

// Use Pinia state
const clubs = computed(() => clubStore.clubs)

const createClub = async () => {
  if (!newClubName.value.trim()) {
    toast.error('Club name is required.')
    return
  }

  try {
    await clubStore.createClub({
      name: newClubName.value.trim(),
      description: newClubDescription.value.trim(),
      is_private: newClubPrivate.value,
    })
    toast.success('Club created successfully!')
    resetCreateModal()
    await messageStore.fetchThreads(true)
  } catch (error) {
    console.error('Create club error:', error)
    toast.error('Failed to create club.')
  }
}

const joinClub = async (clubName) => {
  try {
    await clubStore.joinClub(clubName)
    toast.success(`Successfully joined ${clubName}!`)
  } catch (error) {
    console.error(error)
    toast.error('Failed to join club.')
  }
}

const leaveClub = async (clubName) => {
  try {
    await clubStore.leaveClub(clubName)
    toast.success(`Successfully left ${clubName}.`)

    // Manually set is_member = false for that club
    const club = clubStore.clubs.find(c => c.name === clubName)
    if (club) {
      club.is_member = false
    }
  } catch (error) {
    console.error(error)
    toast.error('Failed to leave club.')
  }
}

const resetCreateModal = () => {
  showCreate.value = false
  newClubName.value = ''
  newClubDescription.value = ''
  newClubPrivate.value = false
}

const goToClub = (clubName) => {
  if (!clubName) {
    toast.error('Invalid club name!')
    return
  }
  router.push(`/clubs/${encodeURIComponent(clubName)}`)
}

const acceptInvite = async (inviteId) => {
  try {
    await inviteStore.acceptInvite(inviteId)
    toast.success('Invite accepted! You joined the club.')
    await clubStore.fetchClubs(true)
  } catch (err) {
    console.error(err)
    toast.error('Failed to accept invite.')
  }
}

const rejectInvite = async (inviteId) => {
  try {
    await inviteStore.rejectInvite(inviteId)
    toast.success('Invite rejected.')
  } catch (err) {
    console.error(err)
    toast.error('Failed to reject invite.')
  }
}

const requestDeleteClub = (clubName) => {
  clubToDelete.value = clubName
  showDeleteConfirm.value = true
}

const confirmDeleteClub = async () => {
  try {
    await authAxios.delete(`/clubs/${encodeURIComponent(clubToDelete.value)}/delete/`)
    toast.success('Club deleted.')
    await clubStore.fetchClubs(true)
    await messageStore.fetchThreads(true)
  } catch (error) {
    console.error(error)
    toast.error('Failed to delete club.')
  } finally {
    showDeleteConfirm.value = false
    clubToDelete.value = null
  }
}


onMounted(() => {
  clubStore.fetchClubs() // only refetch if needed
  inviteStore.fetchInvites()
})
</script>
  
  <style scoped>

  </style>
  