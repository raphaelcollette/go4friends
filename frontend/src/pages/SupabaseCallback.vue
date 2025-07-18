<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex items-center justify-center px-6 max-w-7xl mx-auto w-full">
      <section class="text-center glossy-bg p-8 rounded-2xl shadow-xl">
        <h2 class="text-3xl font-bold text-gray-800 mb-4">🔐 Logging In</h2>
        <p class="text-gray-600 text-lg">Please wait while we authenticate your session...</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/supabase'
import { base } from '@/utils/axios'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  const { data, error } = await supabase.auth.getSession()
  if (error || !data.session) return console.error('No session found')

  const user = data.session.user

  try {
    const res = await base.post('/users/supabase-login/', {
      email: user.email,
      full_name: user.user_metadata.full_name,
      supabase_id: user.id,
    })

    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)

    // Refresh user state after login
    await userStore.fetchCurrentUser()

    router.push('/main')
  } catch (e) {
    console.error('Login failed:', e)
  }
})
</script>