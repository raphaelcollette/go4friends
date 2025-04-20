<template>
  <div>
    <Navbar />

    <div class="flex flex-col items-center justify-center min-h-screen pt-20">
      <div v-if="user" class="bg-white p-6 rounded shadow w-96">
        <h1 class="text-2xl font-bold mb-4">Welcome {{ user.username }}</h1>
        <p class="mb-2">Email: {{ user.email }}</p>
        <button class="btn w-full mt-4" @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/utils/axios'
import Navbar from '@/components/Navbar.vue' 

const user = ref(null)
const router = useRouter()

const fetchUser = async () => {
  try {
    const res = await axios.get('me/')
    user.value = res.data
  } catch (error) {
    router.push('/login')
  }
}

const logout = () => {
  localStorage.removeItem('access_token')
  router.push('/')
}

onMounted(fetchUser)
</script>
