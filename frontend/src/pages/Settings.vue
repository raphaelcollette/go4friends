<template>
    <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
      <Navbar />
  
      <main class="flex-1 flex flex-col items-center pt-24 px-6">
        <div class="bg-white/20 backdrop-blur-md rounded-2xl shadow-lg p-8 w-full max-w-md text-center">
          <h1 class="text-3xl font-bold text-gray-800 mb-6">Settings</h1>
  
          <div class="space-y-6 text-left">
            <div>
              <h2 class="text-lg font-semibold text-gray-700">Account</h2>
              <RouterLink to="/profile/edit" class="text-purple-600 hover:text-purple-800 block mt-2">Edit Profile</RouterLink>
            </div>
  
            <div>
              <h2 class="text-lg font-semibold text-gray-700">Security</h2>
              <button @click="logout" class="btn w-full mt-2">Logout</button>
            </div>
  
            <div>
              <h2 class="text-lg font-semibold text-gray-700">Coming Soon</h2>
              <p class="text-gray-500 text-sm mt-1">Password change, account deletion, and more!</p>
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
  
  const logout = () => {
    localStorage.removeItem('access_token')
    toast.success('Logged out successfully!')
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .btn {
    @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300;
  }
  </style>
  