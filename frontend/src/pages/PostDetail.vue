<template>
  <div class="p-4">
    <div v-if="loading">Loading...</div>
    <div v-else-if="post">
      <h2 class="text-xl font-semibold mb-2">
        {{ post.isAnonymous ? 'Anonymous' : post.author.username }}
      </h2>
      <p class="mb-4">{{ post.content }}</p>
      <p class="text-sm text-gray-500">{{ new Date(post.created_at).toLocaleString() }}</p>
      <!-- Add more fields like likes, reposts, replies as needed -->
    </div>
    <div v-else>
      <p>Post not found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authAxios } from '@/utils/axios'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await authAxios.get(`/posts/${route.params.id}/`)
    post.value = response.data
  } catch (error) {
    console.error('Failed to load post:', error)
  } finally {
    loading.value = false
  }
})
</script>