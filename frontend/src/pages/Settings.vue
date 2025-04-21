<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 w-full max-w-md text-center">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">Settings</h1>

        <div class="space-y-8 text-left">
          <!-- Account Settings -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Account</h2>
            <button @click="editProfile" class="btn w-full mt-2">Edit Profile</button>
            <button @click="changePassword" class="btn w-full mt-2">Change Password</button>
          </div>

          <!-- Security -->
          <div>
            <h2 class="text-lg font-semibold text-gray-700">Security</h2>
            <button @click="logout" class="btn w-full mt-2">Logout</button>
            <button @click="deleteAccount" class="btn w-full mt-2 bg-red-600 hover:bg-red-700">Delete Account</button>
          </div>

          <!-- Preferences -->
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
  </div>
  </template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()
const toast = useToast()

const editProfile = () => {
  router.push('/profile/edit')
}

const logout = () => {
  localStorage.removeItem('access_token')
  toast.success('Logged out successfully!')
  router.push('/login')
}

const changePassword = () => {
  toast.info('Change password feature coming soon!')
}

const deleteAccount = () => {
  toast.warning('Delete account feature coming soon! Be careful!')
}

const toggleDarkMode = () => {
  toast.info('Dark mode toggle coming soon!')
}
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
}
</style>