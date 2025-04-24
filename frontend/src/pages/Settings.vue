<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 w-full max-w-md text-center">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Settings</h1>

        <div class="space-y-8 text-left">
          <!-- Account Settings -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Account</h2>
            <button @click="editProfile" class="btn w-full mt-2">Edit Profile</button>
            <button @click="toggleChangePassword" class="btn w-full mt-2">Change Password</button>
          </div>

          <!-- Show change password form if toggled -->
          <div v-if="showChangePassword" class="space-y-4 mt-4">
            <input v-model="oldPassword" type="password" placeholder="Current Password" class="input w-full" />
            <input v-model="newPassword" type="password" placeholder="New Password (min 8 chars)" class="input w-full" />
            <button @click="submitChangePassword" class="btn w-full mt-2">Submit Password Change</button>
          </div>

          <!-- Security -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Security</h2>
            <button @click="logout" class="btn w-full mt-2">Logout</button>
            <button @click="openDeleteModal" class="btn w-full mt-2 bg-red-600 hover:bg-red-700">Delete Account</button>
          </div>

          <!-- Preferences -->
          
          <!-- Privacy Settings -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Privacy</h2>
            <div class="flex items-center justify-between mt-2">
              <label class="text-sm text-gray-700">Private Profile</label>
              <input type="checkbox" v-model="isPrivate" @change="updatePrivacy" class="form-checkbox h-5 w-5 text-purple-600">
            </div>
          </div>
          
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Preferences</h2>
            <button @click="toggleDarkMode" class="btn w-full mt-2">Toggle Dark Mode</button>
          </div>

          <!-- Notifications (coming soon) -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Notifications</h2>
            <p class="text-gray-500 text-sm mt-1">Manage notification settings (coming soon)</p>
          </div>

          <!-- About -->
          <div class="pt-6 border-t border-white/30">
            <p class="text-xs text-gray-500 mt-4 text-center">
              go4friends app v1.0 — Built with ❤️ by You
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-lg p-6 w-80 text-center">
        <h2 class="text-xl font-bold text-red-600 mb-4">Delete Account</h2>
        <p class="text-gray-600 mb-6">Are you sure you want to permanently delete your account? This action cannot be undone.</p>
        <div class="flex space-x-4 justify-center">
          <button @click="confirmDeleteAccount" class="btn bg-red-600 hover:bg-red-700 w-full">Yes, Delete</button>
          <button @click="cancelDelete" class="btn bg-gray-300 hover:bg-gray-400 text-gray-800 w-full">Cancel</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { ref, watch, onMounted } from 'vue'
import { authAxios } from '@/utils/axios'
import { useUserStore } from '@/stores/user' // ✅ Import the Pinia store
import { useFriendStore } from '@/stores/friend'
import { useMessageStore } from '@/stores/messages'
import { useClubStore } from '@/stores/club'
import { useEventStore } from '@/stores/events'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const showChangePassword = ref(false)
const oldPassword = ref('')
const newPassword = ref('')

const isPrivate = ref(false)

const toggleChangePassword = () => {
  showChangePassword.value = !showChangePassword.value
}

const submitChangePassword = async () => {
  if (newPassword.value.length < 8) {
    toast.error('New password must be at least 8 characters long.')
    return
  }

  try {
    await authAxios.patch('/users/change-password/', {
      old_password: oldPassword.value,
      new_password: newPassword.value
    })
    
    toast.success('Password changed successfully! Please log in again.')
    showChangePassword.value = false
    oldPassword.value = ''
    newPassword.value = ''
    localStorage.removeItem('access_token')
    router.push('/login')
  } catch (error) {
    toast.error(error.response?.data?.error || 'Failed to change password.')
  }
}

const editProfile = () => {
  router.push('/profile/edit')
}

const logout = () => {
  localStorage.removeItem('access_token')

  // Reset all user-related stores
  useUserStore().reset()
  useFriendStore().reset()
  useMessageStore().reset()
  useClubStore().reset()
  useEventStore().reset()

  toast.success('Logged out successfully!')
  router.push('/login')
}

const showDeleteModal = ref(false)

const openDeleteModal = () => {
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
}

const confirmDeleteAccount = async () => {
  try {
    await authAxios.delete('/users/delete-account/')
    toast.success('Account deleted successfully.')
    localStorage.removeItem('access_token')
    router.push('/signup')
  } catch (error) {
    toast.error('Failed to delete account. Please try again.')
  } finally {
    showDeleteModal.value = false
  }
}

const toggleDarkMode = () => {
  toast.info('Dark mode toggle coming soon!')
}

const updatePrivacy = async () => {
  try {
    await authAxios.patch('/users/me/update/', { is_private: isPrivate.value })
    toast.success('Privacy setting updated.')
    await userStore.fetchCurrentUser()
  } catch (e) {
    toast.error('Failed to update privacy.')
  }
}

// Sync privacy checkbox with store
watch(
  () => userStore.currentUser,
  (user) => {
    if (user) isPrivate.value = user.is_private
  },
  { immediate: true }
)

onMounted(() => {
  userStore.fetchCurrentUser()
})
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
.input {
  @apply p-2 rounded-lg bg-white/50 backdrop-blur-sm placeholder-gray-500 text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-400;
}
</style>

