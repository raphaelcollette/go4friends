<template>
  <div class="landing-container">
    <Navbar />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'  // 
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

const user = ref(null)
const router = useRouter()
const toast = useToast()

const fetchUser = async () => {
  try {
    const res = await authAxios.get('users/me/')  //
    user.value = res.data
  } catch (error) {
    router.push('/login')  // If not logged in, kick back to login
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  toast.success('You have been logged out.')
  router.push('/login')
}

onMounted(fetchUser)

</script>

<style scoped>
/* Layout background (gradient) */
.landing-container {
  @apply flex flex-col min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100;
}

/* Button styles */
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl text-lg transition-all duration-300;
}
</style>
