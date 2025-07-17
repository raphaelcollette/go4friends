<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 max-w-7xl mx-auto w-full gap-8" style="height: calc(100vh - 6rem);">

      <section class="flex-1 flex flex-col h-full">
        <section class="w-full flex flex-col flex-grow overflow-hidden">
          <div class="text-center mb-8 flex-shrink-0">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">📱 Post Detail</h2>
          </div>

          <div class="glossy-bg rounded-2xl shadow-lg p-6 mb-6 flex-shrink-0" v-if="loading">
            Loading...
          </div>

          <div v-else-if="post" class="glossy-bg rounded-2xl shadow-lg p-6 mb-6 flex-shrink-0">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span class="text-white font-bold text-lg">{{ post.authorInitials || 'A' }}</span>
              </div>
              <div class="flex-1">
                <div class="flex items-center space-x-2 mb-2">
                  <h4 class="font-bold text-gray-800">
                    {{ post.is_anonymous ? 'Anonymous' : post.username }}
                  </h4>
                  <span class="text-gray-500 text-sm">@{{ post.username }}</span>
                  <span class="text-gray-400 text-sm">·</span>
                  <span class="text-gray-500 text-sm">{{ post.timeAgo }}</span>
                </div>
                <p class="text-gray-700 mb-3 leading-relaxed">{{ post.content }}</p>
                <div class="flex items-center space-x-6 text-gray-500">
                  <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                    <span>💬</span>
                    <span class="text-sm">{{ post.commentCount }}</span>
                  </button>
                  <button
                    v-if="!post.hasLiked"
                    class="flex items-center space-x-2 hover:text-red-500 transition-colors"
                    @click="likePost(post.id)"
                  >
                    <span>❤️</span>
                    <span class="text-sm">{{ post.likeCount }}</span>
                  </button>
                  <button
                    v-else
                    class="flex items-center space-x-2 text-red-500 transition-colors"
                    @click="unlikePost(post.id)"
                  >
                    <span>🗑️❤️</span>
                    <span class="text-sm">{{ post.likeCount }}</span>
                  </button>
                  <button
                    v-if="!post.hasReposted"
                    class="flex items-center space-x-2 hover:text-green-500 transition-colors"
                    @click="repostPost(post.id)"
                  >
                    <span>🔁</span>
                    <span class="text-sm">{{ post.repostCount }}</span>
                  </button>
                  <button
                    v-else
                    class="flex items-center space-x-2 text-green-600 transition-colors"
                    @click="undoRepostPost(post.id)"
                  >
                    <span>🗑️🔁</span>
                    <span class="text-sm">{{ post.repostCount }}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-else>
            <p class="text-center text-gray-500 select-none">Post not found.</p>
          </div>
        </section>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authAxios } from '@/utils/axios'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

const likePost = async (postId) => {
  try {
    await authAxios.post(`/posts/${postId}/like/`)
    if (post.value && post.value.id === postId) {
      post.value.hasLiked = true
      post.value.likeCount = (post.value.likeCount || 0) + 1
    }
  } catch (e) {
    console.error(e)
  }
}

const unlikePost = async (postId) => {
  try {
    await authAxios.post(`/posts/${postId}/unlike/`)
    if (post.value && post.value.id === postId) {
      post.value.hasLiked = false
      post.value.likeCount = Math.max((post.value.likeCount || 1) - 1, 0)
    }
  } catch (e) {
    console.error(e)
  }
}

const repostPost = async (postId) => {
  try {
    await authAxios.post(`/posts/${postId}/repost/`)
    if (post.value && post.value.id === postId) {
      post.value.hasReposted = true
      post.value.repostCount = (post.value.repostCount || 0) + 1
    }
  } catch (e) {
    console.error(e)
  }
}

const undoRepostPost = async (postId) => {
  try {
    await authAxios.delete(`/posts/${postId}/undo_repost/`)
    if (post.value && post.value.id === postId) {
      post.value.hasReposted = false
      post.value.repostCount = Math.max((post.value.repostCount || 1) - 1, 0)
    }
  } catch (e) {
    console.error(e)
  }
}

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
