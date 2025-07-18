<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/supabase'
import { base } from '@/axios'

const router = useRouter()

onMounted(async () => {
  const { data, error } = await supabase.auth.getSession()
  if (error || !data.session) return console.error('No session found')

  const user = data.session.user

  const res = await base.post('/users/supabase-login/', {
    email: user.email,
    full_name: user.user_metadata.full_name,
    supabase_id: user.id,
  })

  localStorage.setItem('access_token', res.data.access)
  localStorage.setItem('refresh_token', res.data.refresh)
  router.push('/')
})
</script>

<template>
  <div>Logging in...</div>
</template>