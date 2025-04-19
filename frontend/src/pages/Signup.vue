<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <form @submit.prevent="signup" class="bg-white p-6 rounded shadow w-96">
      <h1 class="text-2xl mb-4 font-bold">Sign Up</h1>
      <input v-model="email" type="email" placeholder="Email" class="input" />
      <input v-model="username" type="text" placeholder="Username" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />
      <button class="btn mt-4 w-full">Create Account</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'

const email = ref('')
const username = ref('')
const password = ref('')
const router = useRouter()

const signup = async () => {
  try {
    await axios.post('signup/', {
      email: email.value,
      username: username.value,
      password: password.value,
    })
    router.push('/login')
  } catch (error) {
    alert('Signup failed.')
  }
}
</script>
