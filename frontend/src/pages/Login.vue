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
                <div class="relative">
                  <input id="remember-me" type="checkbox" class="checkbox" />
                  <svg class="checkbox-icon" viewBox="0 0 16 16" fill="none">
                    <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" fill="currentColor"/>
                  </svg>
                </div>
                <label for="remember-me" class="ml-4 block text-sm font-medium text-gray-700 cursor-pointer select-none">Remember me</label>
              </div>
              <a href="#" class="text-sm font-medium text-[color:var(--btn-primary)] hover:text-[color:var(--btn-primary-hover)] transition-colors duration-200">Forgot password?</a>
            </div>

            <button type="submit" class="btn btn-primary">
              <span class="btn-content">
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                Sign in
              </span>
            </button>
          </form>

          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4 bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 text-gray-500">or continue with</span>
            </div>
          </div>

          <button @click="loginWithGoogle" class="btn btn-google">
            <span class="btn-content">
              <svg class="btn-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="#4285f4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34a853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#fbbc05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#ea4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Continue with Google
            </span>
          </button>

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

/* Enhanced Checkbox */
.checkbox {
  appearance: none;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  flex-shrink: 0;
}

.checkbox:hover {
  border-color: var(--btn-primary);
  background-color: rgba(99, 102, 241, 0.05);
}

.checkbox:checked {
  background-color: var(--btn-primary);
  border-color: var(--btn-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.checkbox:checked:focus {
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

.checkbox-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0.75rem;
  height: 0.75rem;
  color: white;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.checkbox:checked + .checkbox-icon {
  opacity: 1;
}

/* Enhanced Buttons */
.btn {
  width: 100%;
  padding: 0;
  border: none;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.1);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.1);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  min-height: 3.25rem;
}

.btn-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Primary Button */
.btn-primary {
  color: white;
  background: linear-gradient(135deg, var(--btn-primary) 0%, var(--btn-primary-hover) 100%);
  margin-bottom: 0.5rem;
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--btn-primary-hover) 0%, var(--btn-primary) 100%);
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover::before {
  left: 100%;
}

/* Google Button */
.btn-google {
  color: #374151;
  background: white;
  border: 2px solid #e5e7eb;
  position: relative;
}

.btn-google:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.btn-google::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(66, 133, 244, 0.1), transparent);
  transition: left 0.5s;
}

.btn-google:hover::before {
  left: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .btn-content {
    padding: 0.875rem 1.25rem;
    min-height: 3rem;
  }
  
  .btn-icon {
    width: 18px;
    height: 18px;
  }
}
</style>