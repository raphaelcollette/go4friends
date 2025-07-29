<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div class="glossy-bg rounded-2xl shadow-lg p-8 w-full max-w-md text-center">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Settings</h1>

        <div class="space-y-8 text-left">
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Account</h2>
            <button @click="editProfile" class="btn w-full mt-2">Edit Profile</button>
            <button @click="toggleChangePassword" class="btn w-full mt-2">Change Password</button>
            <button @click="toggleChangeUsername" class="btn w-full mt-2">Change Username</button>
          </div>

          <div v-if="showChangePassword" class="space-y-4 mt-4">
            <input v-model="oldPassword" type="password" placeholder="Current Password" class="input w-full" />
            <input v-model="newPassword" type="password" placeholder="New Password (min 8 chars)" class="input w-full" />
            <button @click="submitChangePassword" class="btn w-full mt-2">Submit Password Change</button>
          </div>

          <div v-if="showChangeUsername" class="space-y-4 mt-4">
            <input v-model="newUsername" type="text" placeholder="New Username" class="input w-full" />
            <button @click="submitChangeUsername" class="btn w-full mt-2">Submit Username Change</button>
          </div>

          <div>
            <h2 class="text-lg font-semibold text-gray-700">Security</h2>
            <button @click="logout" class="btn w-full mt-2">Logout</button>
            <button @click="openDeleteModal" class="btn w-full mt-2 bg-red-600 hover:bg-red-700">Delete Account</button>
          </div>

          <div>
            <h2 class="text-lg font-semibold text-gray-700">Privacy</h2>
            <div class="flex items-center justify-between mt-2">
              <label class="text-sm text-gray-700">Private Profile</label>
              <input type="checkbox" v-model="isPrivate" @change="updatePrivacy" class="form-checkbox h-5 w-5 text-purple-600">
            </div>
          </div>

          <div>
            <h2 class="text-lg font-semibold text-gray-700">Preferences</h2>
            <div class="mt-6">
              <h2 class="text-lg font-semibold text-gray-700">Theme Color</h2>
              <div class="flex items-center space-x-4 mt-2">
                <div class="relative w-12 h-12">
                  <input type="color" v-model="userColor" @input="updateColor" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                  <div class="w-full h-full rounded-full border-2 border-gray-300" :style="{ backgroundColor: userColor }"></div>
                </div>
                <span class="text-gray-600 text-sm">Choose your button color</span>
              </div>
            </div>

            <div class="mt-6">
              <h2 class="text-lg font-semibold text-gray-700">Secondary Color</h2>
              <div class="flex items-center space-x-4 mt-2">
                <div class="relative w-12 h-12">
                  <input type="color" v-model="userSecondaryColor" @input="updateSecondaryColor" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                  <div class="w-full h-full rounded-full border-2 border-gray-300" :style="{ backgroundColor: userSecondaryColor }"></div>
                </div>
                <span class="text-gray-600 text-sm">Choose your secondary color</span>
              </div>
            </div>
            <button @click="resetTheme" class="btn w-full mt-2">Reset to Default</button>
          </div>

          <div class="pt-6 border-t border-white/30">
            <p class="text-xs text-gray-500 mt-4 text-center">
              go4friends app v1.0 — Built by RC
            </p>
          </div>
        </div>
      </div>
    </main>

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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { authAxios } from '@/utils/axios'
import { useUserStore } from '@/stores/user'
import { useFriendStore } from '@/stores/friend'
import { useMessageStore } from '@/stores/messages'
import { useClubStore } from '@/stores/club'
import { useEventStore } from '@/stores/events'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const showChangeUsername = ref(false)
const newUsername = ref('')
const showChangePassword = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const userColor = ref(localStorage.getItem('userColor') || '#7A0019')
const userSecondaryColor = ref(localStorage.getItem('userSecondaryColor') || '#FFCC33')
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const isPrivate = ref(false)

const applyTheme = () => {
  document.documentElement.style.setProperty('--btn-primary', userColor.value)
  document.documentElement.style.setProperty('--btn-primary-hover', darkenColor(userColor.value, 10))
  document.documentElement.style.setProperty('--btn-secondary', userSecondaryColor.value)

  if (isDarkMode.value) {
    document.documentElement.style.setProperty('--page-background', 'linear-gradient(to bottom right, #1f2937, #4b5563, #6b7280)')
  } else {
    document.documentElement.style.setProperty('--page-background', 'linear-gradient(to bottom right, #dbeafe, #ede9fe, #fce7f3)')
  }
}

const toggleChangePassword = () => {
  showChangePassword.value = !showChangePassword.value
}

const submitChangeUsername = async () => {
  if (!newUsername.value.trim()) {
    toast.error('Username cannot be empty.')
    return
  }
  try {
    await authAxios.patch('/users/me/update/', { username: newUsername.value })
    toast.success('Username updated! Logging out...')
    // Clear user data and tokens
    localStorage.removeItem('access_token')
    userStore.reset()
    // Redirect to login
    router.push('/login')
  } catch {
    toast.error('Failed to update username.')
  }
}

const toggleChangeUsername = () => {
  showChangeUsername.value = !showChangeUsername.value
}

const submitChangePassword = async () => {
  if (newPassword.value.length < 8) {
    toast.error('New password must be at least 8 characters.')
    return
  }
  try {
    await authAxios.patch('/users/change-password/', { old_password: oldPassword.value, new_password: newPassword.value })
    toast.success('Password changed!')
    router.push('/login')
  } catch (e) {
    toast.error('Failed to change password.')
  }
}

const editProfile = () => router.push('/profile/edit')

const logout = () => {
  localStorage.removeItem('access_token')
  useUserStore().reset()
  useFriendStore().reset()
  useMessageStore().reset()
  useClubStore().reset()
  useEventStore().reset()
  router.push('/login')
}

const showDeleteModal = ref(false)
const openDeleteModal = () => showDeleteModal.value = true
const cancelDelete = () => showDeleteModal.value = false

const confirmDeleteAccount = async () => {
  try {
    await authAxios.delete('/users/delete-account/')
    router.push('/signup')
  } catch {
    toast.error('Failed to delete account.')
  }
}

const resetTheme = () => {
  userColor.value = '#7A0019'
  userSecondaryColor.value = '#FFCC33'
  isDarkMode.value = false
  localStorage.removeItem('darkMode')
  localStorage.removeItem('userColor')
  localStorage.removeItem('userSecondaryColor')
  applyTheme()
}

const updateColor = () => {
  localStorage.setItem('userColor', userColor.value)
  applyTheme()
}

const updateSecondaryColor = () => {
  localStorage.setItem('userSecondaryColor', userSecondaryColor.value)
  applyTheme()
}

const darkenColor = (hex, percent) => {
  const num = parseInt(hex.replace("#", ""), 16)
  const amt = Math.round(2.55 * percent)
  const R = (num >> 16) - amt
  const G = (num >> 8 & 0x00FF) - amt
  const B = (num & 0x0000FF) - amt
  return `#${(0x1000000 + (R<255?(R<1?0:R):255)*0x10000 + (G<255?(G<1?0:G):255)*0x100 + (B<255?(B<1?0:B):255)).toString(16).slice(1)}`
}

const updatePrivacy = async () => {
  try {
    await authAxios.patch('/users/me/update/', { is_private: isPrivate.value })
    toast.success('Privacy updated!')
    userStore.fetchCurrentUser()
  } catch {
    toast.error('Failed to update privacy.')
  }
}

watch(() => userStore.currentUser, (user) => {
  if (user) isPrivate.value = user.is_private
}, { immediate: true })

onMounted(() => {
  applyTheme()
})
</script>

<style scoped>
</style>