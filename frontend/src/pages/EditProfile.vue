<template>
    <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
      <Navbar />
  
      <main class="flex-1 flex items-center justify-center pt-24 px-4">
        <div class="bg-white/20 backdrop-blur-md rounded-2xl p-8 w-full max-w-lg shadow-lg">
          <h1 class="text-3xl font-extrabold text-center text-gray-800 mb-8">Edit Profile</h1>
  
          <form @submit.prevent="updateProfile" class="space-y-6">
            <div class="flex flex-col space-y-2">
              <label class="text-sm font-medium text-gray-700">Full Name</label>
              <input v-model="full_name" type="text" class="input" placeholder="Enter your full name" />
            </div>
  
            <div class="flex flex-col space-y-2">
              <label class="text-sm font-medium text-gray-700">Bio</label>
              <textarea v-model="bio" rows="3" class="input" placeholder="Tell us about yourself..."></textarea>
            </div>
  
            <div class="flex flex-col space-y-2">
              <label class="text-sm font-medium text-gray-700">Location</label>
              <input v-model="location" type="text" class="input" placeholder="Where are you?" />
            </div>
  
            <div class="flex flex-col space-y-2">
              <label class="text-sm font-medium text-gray-700">Profile Picture URL</label>
              <input v-model="profile_picture" type="text" class="input" placeholder="Paste image URL (for now)" />
            </div>
  
            <div class="flex justify-between items-center mt-8">
              <button type="button" @click="cancel" class="btn bg-gray-400 hover:bg-gray-500">Cancel</button>
              <button type="submit" class="btn">Save Changes</button>
            </div>
          </form>
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { authAxios } from '@/utils/axios'
  import Navbar from '@/components/Navbar.vue'
  import { useToast } from 'vue-toastification'
  
  const router = useRouter()
  const toast = useToast()
  
  const full_name = ref('')
  const bio = ref('')
  const location = ref('')
  const profile_picture = ref('')
  
  const fetchProfile = async () => {
    try {
      const res = await authAxios.get('users/me/')
      full_name.value = res.data.full_name || ''
      bio.value = res.data.bio || ''
      location.value = res.data.location || ''
      profile_picture.value = res.data.profile_picture || ''
    } catch (error) {
      console.error('Failed to fetch profile:', error)
      toast.error('Failed to load your profile.')
      router.push('/profile')
    }
  }
  
  const updateProfile = async () => {
    try {
      await authAxios.patch('users/me/update/', {
        full_name: full_name.value,
        bio: bio.value,
        location: location.value,
        profile_picture: profile_picture.value,
      })
      toast.success('Profile updated successfully!')
      router.push('/profile')
    } catch (error) {
      console.error('Failed to update profile:', error)
      toast.error('Failed to update profile.')
    }
  }
  
  const cancel = () => {
    router.push('/profile')
  }
  
  onMounted(fetchProfile)
  </script>
  
  <style scoped>
  .input {
    @apply w-full bg-white border border-gray-300 rounded-xl p-4 text-lg focus:outline-none focus:ring-2 focus:ring-purple-400;
  }
  
  .btn {
    @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300;
  }
  </style>
  