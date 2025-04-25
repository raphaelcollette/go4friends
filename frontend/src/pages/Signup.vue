<template>
  <div class="landing-container">
    <!-- Left Side: Full Image -->
    <div class="w-1/2 h-full">
      <img src="@/assets/bridge.webp" alt="bridge at sunset" class="w-full h-full object-cover" />
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
              <input id="email" type="email" v-model="email" class="login-input" placeholder="Enter your email" />
            </div>

            <div class="space-y-2">
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input id="username" type="text" v-model="username" class="login-input" placeholder="Choose a username" />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input id="password" type="password" v-model="password" class="login-input" placeholder="Create a password" />
            </div>

            <button type="submit" class="btn w-full mt-4">
              Create Account
            </button>
          </form>

          <div class="pt-8">
            <p class="text-center text-gray-600 text-sm">
              Already have an account?
              <RouterLink to="/login" class="text-[color:var(--btn-primary)] font-medium hover:text-[color:var(--btn-primary-hover)]">
                Log in
              </RouterLink>
            </p>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { base } from '@/utils/axios'
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
    await base.post('users/signup/', {
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

/* Inputs */
.login-input {
  @apply w-full bg-white/90 border border-gray-300 placeholder-gray-500 text-gray-800 px-6 py-4 text-base leading-7 rounded-2xl transition-all duration-300 focus:outline-none;
  min-height: 3.25rem;
  font-size: 1rem;
  line-height: 1.75rem;
}
.login-input:focus {
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 0 0 4px var(--btn-primary);
  border-color: var(--btn-primary);
}

/* Button */
.btn {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  font-weight: 600;
  color: white;
  background-color: var(--btn-primary);
  transition: all 0.3s ease;
}
.btn:hover {
  background-color: var(--btn-primary-hover);
}
</style>
