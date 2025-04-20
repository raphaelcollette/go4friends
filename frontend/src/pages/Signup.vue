<template>
  <div class="landing-container">
    <!-- Left Side: Full Image -->
    <div class="w-1/2 h-full">
      <img src="@/assets/bridge.png" alt="bridge at sunset" class="w-full h-full object-cover" />
    </div>

    <!-- Right Side: Signup Form -->
    <div class="w-1/2 h-full bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex items-center justify-center p-4">
      <transition name="fade">
        <div v-if="showForm" class="w-full max-w-md p-8">
          <h1 class="text-4xl font-extrabold text-gray-800 mb-4 text-center">Create Account</h1>
          <p class="text-gray-500 mb-10 text-center">Please enter your details to sign up</p>

          <form @submit.prevent="signup" class="space-y-6">
            <div class="space-y-2">
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input id="email" type="email" v-model="email" class="input" placeholder="Enter your email" />
            </div>

            <div class="space-y-2">
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input id="username" type="text" v-model="username" class="input" placeholder="Choose a username" />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input id="password" type="password" v-model="password" class="input" placeholder="Create a password" />
            </div>

            <button type="submit" class="btn w-full mt-4">
              Create Account
            </button>
          </form>

          <div class="pt-8">
            <p class="text-center text-gray-600 text-sm">
              Already have an account?
              <RouterLink to="/login" class="text-purple-600 font-medium hover:text-purple-500">Log in</RouterLink>
            </p>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const email = ref('')
const username = ref('')
const password = ref('')
const showForm = ref(false)
const router = useRouter()
const toast = useToast()

onMounted(() => {
  showForm.value = true
})

const signup = async () => {
  try {
    await axios.post('signup/', {
      email: email.value,
      username: username.value,
      password: password.value,
    })
    toast.success('Account created! You can now log in.')
    router.push('/login')
  } catch (error) {
    toast.error('Signup failed. Please try again.')
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

/* Transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
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
