<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <form @submit.prevent="login" class="bg-white p-6 rounded shadow w-96">
      <h1 class="text-2xl mb-4 font-bold">Login</h1>
      <input v-model="username" type="text" placeholder="Username" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />
      <button class="btn mt-4 w-full">Log In</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('login/', {
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('access_token', res.data.access)
    router.push('/profile')
  } catch (error) {
    alert('Login failed.')
  }
}
</script>