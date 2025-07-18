<template>
  <div class="landing-container">
    <!-- Left Side: Full Image -->
    <div class="w-1/2 h-full">
      <img src="@/assets/middlebrook.webp" alt="city from middlebrook" class="w-full h-full object-cover" />
    </div>

    <!-- Right Side: Login Form -->
    <div class="w-1/2 h-full bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex items-center justify-center p-4">
      <transition name="fade">
        <div v-if="showForm" class="w-full max-w-md p-8">
          <h1 class="text-4xl font-extrabold text-gray-800 mb-4 text-center">Welcome back</h1>
          <p class="text-gray-500 mb-10 text-center">Please enter your details to sign in</p>

          <form @submit.prevent="login" class="space-y-6">
            <div class="space-y-2">
              <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
              <input id="username" type="text" v-model="username" class="login-input" placeholder="Enter your username" />
            </div>

            <div class="space-y-2">
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input id="password" type="password" v-model="password" class="login-input" placeholder="Enter your password" />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input id="remember-me" type="checkbox" class="checkbox" />
                <label for="remember-me" class="ml-2 block text-sm text-gray-700">Remember me</label>
              </div>
              <a href="#" class="text-sm font-medium text-[color:var(--btn-primary)] hover:text-[color:var(--btn-primary-hover)]">Forgot password?</a>
            </div>

            <button type="submit" class="btn w-full">
              Sign in
            </button>
            <button @click="loginWithGoogle" class="btn btn-google">
              Sign in with Google
            </button>
          </form>

          <div class="pt-8">
            <p class="text-center text-gray-600 text-sm">
              Don't have an account?
              <RouterLink to="/signup" class="text-[color:var(--btn-primary)] font-medium hover:text-[color:var(--btn-primary-hover)]">Sign up</RouterLink>
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
import { jwtDecode } from 'jwt-decode'
import { supabase } from '@/supabase'

const username = ref('')
const password = ref('')
const showForm = ref(false)
const router = useRouter()
const toast = useToast()

onMounted(() => {
  showForm.value = true
})

const login = async () => {
  try {
    const res = await base.post('users/login/', {
      username: username.value,
      password: password.value,
    })

    // Save tokens
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)

    // Decode access token to extract username
    const decoded = jwtDecode(res.data.access)
    localStorage.setItem('currentUsername', decoded.username)

    toast.success('Successfully logged in!')
    router.push('/main')
  } catch (error) {
    toast.error('Login failed. Please check your username/password.')
  }
}

const loginWithGoogle = async () => {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: 'https://go4friends.vercel.app/auth/callback',
  },
  })
  if (error) console.error('OAuth error:', error.message)
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

/* Checkbox */
.checkbox {
  @apply h-5 w-5 border-gray-300 rounded focus:ring-2;
  color: var(--btn-primary);
}
.checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--btn-primary);
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
