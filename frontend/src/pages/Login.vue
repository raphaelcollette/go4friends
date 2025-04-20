<template>
  <div class="landing-container">
    <!-- Left Side: Full Image -->
    <div class="w-1/2 h-full">
      <img src="@/assets/bridge.png" alt="City at sunset" class="w-full h-full object-cover" />
    </div>
        
    <!-- Right Side: Login Form (transparent) -->
    <div class="w-1/2 h-full bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex items-center justify-center p-4">
      <div class="w-full max-w-md p-8">
        <h1 class="text-4xl font-extrabold text-gray-800 mb-4 text-center">Welcome back</h1>
        <p class="text-gray-500 mb-10 text-center">Please enter your details to sign in</p>
        
        <form @submit.prevent="login" class="space-y-6">
          <div class="space-y-2">
            <label for="username" class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <input
              id="username"
              type="text"
              v-model="username"
              class="input"
              placeholder="Enter your username"
            />
          </div>
          
          <div class="space-y-2">
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              v-model="password"
              class="input"
              placeholder="Enter your password"
            />
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                type="checkbox"
                class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                Remember me
              </label>
            </div>
            <a href="#" class="text-sm font-medium text-purple-600 hover:text-purple-500">
              Forgot password?
            </a>
          </div>

          <button type="submit" class="btn w-full">
            Sign in
          </button>
        </form>

        <div class="pt-8">
          <p class="text-center text-gray-600 text-sm">
            Don't have an account?
            <RouterLink to="/signup" class="text-purple-600 font-medium hover:text-purple-500">
              Sign up
            </RouterLink>
          </p>
        </div>
      </div>
    </div>
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
    router.push('/main')
  } catch (error) {
    alert('Login failed.')
  }
}
</script>

<style scoped>
/* Layout */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  width: 100%;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

.landing-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Buttons */
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl text-lg transition-all duration-300;
}

/* Inputs */
.input {
  @apply w-full bg-white border border-gray-300 rounded-xl p-4 text-lg focus:outline-none focus:ring-2 focus:ring-purple-400;
}
</style>
