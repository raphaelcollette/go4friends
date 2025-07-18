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
              <div v-if="post.user?.profile_picture_url" class="flex-shrink-0">
                <img
                  :src="post.user.profile_picture_url"
                  alt="Profile Picture"
                  class="w-12 h-12 rounded-full object-cover border-2 border-purple-400"
                />
              </div>
              <div
                v-else
                class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0"
              >
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

                <div class="flex items-center space-x-6 text-gray-500 mb-4">
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
                  <button
                    v-if="canDeletePost(post)"
                    @click="deletePostHandler(post.id)"
                    class="ml-4 text-red-600 hover:text-red-800 transition-colors"
                    title="Delete post"
                  >
                    🗑️
                  </button>
                </div>

                <!-- Reply Input -->
                <div class="mb-6">
                  <textarea
                    v-model="replyContent"
                    placeholder="Write a reply..."
                    rows="3"
                    class="w-full bg-white/70 rounded-xl p-3 text-gray-800 focus:outline-none resize-none"
                  ></textarea>
                  <div class="flex justify-end mt-2">
                    <button
                      :disabled="isReplying || replyContent.trim() === ''"
                      @click="submitReply"
                      class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 disabled:opacity-50 transition-all"
                    >
                      {{ isReplying ? 'Replying...' : 'Reply' }}
                    </button>
                  </div>
                </div>

                <!-- Replies List -->
                <div v-if="replies.length > 0" class="space-y-4">
                  <div
                    v-for="reply in replies"
                    :key="reply.id"
                    class="border-t pt-4"
                  >
                    <div class="flex items-start space-x-4">
                      <div v-if="reply.user?.profile_picture_url" class="flex-shrink-0">
                        <img
                          :src="reply.user.profile_picture_url"
                          alt="Profile Picture"
                          class="w-10 h-10 rounded-full object-cover border-2 border-purple-400"
                        />
                      </div>
                      <div
                        v-else
                        class="w-10 h-10 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center flex-shrink-0"
                      >
                        <span class="text-white font-semibold">{{ reply.authorInitials || 'A' }}</span>
                      </div>
                      <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1">
                          <h5 class="font-semibold text-gray-800">
                            {{ reply.is_anonymous ? 'Anonymous' : reply.username }}
                          </h5>
                          <span class="text-gray-500 text-xs">@{{ reply.username }}</span>
                          <span class="text-gray-400 text-xs">·</span>
                          <span class="text-gray-500 text-xs">{{ reply.timeAgo }}</span>
                        </div>
                        <p class="text-gray-700 leading-relaxed">{{ reply.content }}</p>

                        <div class="flex items-center space-x-6 text-gray-500 mt-2">
                          <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors" disabled>
                            <span>💬</span>
                            <span class="text-sm">{{ reply.commentCount || 0 }}</span>
                          </button>

                          <button
                            v-if="!reply.hasLiked"
                            class="flex items-center space-x-2 hover:text-red-500 transition-colors"
                            @click="likeReply(reply.id)"
                          >
                            <span>❤️</span>
                            <span class="text-sm">{{ reply.likeCount }}</span>
                          </button>
                          <button
                            v-else
                            class="flex items-center space-x-2 text-red-500 transition-colors"
                            @click="unlikeReply(reply.id)"
                          >
                            <span>🗑️❤️</span>
                            <span class="text-sm">{{ reply.likeCount }}</span>
                          </button>

                          <button
                            v-if="!reply.hasReposted"
                            class="flex items-center space-x-2 hover:text-green-500 transition-colors"
                            @click="repostReply(reply.id)"
                          >
                            <span>🔁</span>
                            <span class="text-sm">{{ reply.repostCount }}</span>
                          </button>
                          <button
                            v-else
                            class="flex items-center space-x-2 text-green-600 transition-colors"
                            @click="undoRepostReply(reply.id)"
                          >
                            <span>🗑️🔁</span>
                            <span class="text-sm">{{ reply.repostCount }}</span>
                          </button>

                          <button
                            v-if="canDeletePost(reply)"
                            @click="deleteReplyHandler(reply.id)"
                            class="ml-4 text-red-600 hover:text-red-800 transition-colors"
                            title="Delete reply"
                          >
                            🗑️
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-gray-500 select-none italic text-sm">No replies yet.</div>
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
const replies = ref([])

const replyContent = ref('')
const isReplying = ref(false)

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

const fetchReplies = async () => {
  try {
    const res = await authAxios.get(`/posts/${route.params.id}/replies/`)
    replies.value = res.data
  } catch (error) {
    console.error('Failed to load replies:', error)
  }
}

const submitReply = async () => {
  if (replyContent.value.trim() === '') return
  isReplying.value = true
  try {
    const res = await authAxios.post('/posts/create/', {
      content: replyContent.value,
      parent: route.params.id,
    })
    replies.value.unshift(res.data)
    replyContent.value = ''
  } catch (error) {
    console.error('Failed to submit reply:', error)
  } finally {
    isReplying.value = false
  }
}

const likeReply = async (replyId) => {
  try {
    await authAxios.post(`/posts/${replyId}/like/`)
    const r = replies.value.find(r => r.id === replyId)
    if (r) {
      r.hasLiked = true
      r.likeCount = (r.likeCount || 0) + 1
    }
  } catch (e) {
    console.error(e)
  }
}

const unlikeReply = async (replyId) => {
  try {
    await authAxios.post(`/posts/${replyId}/unlike/`)
    const r = replies.value.find(r => r.id === replyId)
    if (r) {
      r.hasLiked = false
      r.likeCount = Math.max((r.likeCount || 1) - 1, 0)
    }
  } catch (e) {
    console.error(e)
  }
}

const repostReply = async (replyId) => {
  try {
    await authAxios.post(`/posts/${replyId}/repost/`)
    const r = replies.value.find(r => r.id === replyId)
    if (r) {
      r.hasReposted = true
      r.repostCount = (r.repostCount || 0) + 1
    }
  } catch (e) {
    console.error(e)
  }
}

const undoRepostReply = async (replyId) => {
  try {
    await authAxios.delete(`/posts/${replyId}/undo_repost/`)
    const r = replies.value.find(r => r.id === replyId)
    if (r) {
      r.hasReposted = false
      r.repostCount = Math.max((r.repostCount || 1) - 1, 0)
    }
  } catch (e) {
    console.error(e)
  }
}

const canDeletePost = (postOrReply) => {
  // Implement based on user store or context, simplified example:
  const currentUser = { username: 'raphael' } // Replace with actual user state
  if (!currentUser) return false
  return postOrReply.username === currentUser.username
}

const deletePostHandler = async (postId) => {
  try {
    await authAxios.delete(`/posts/${postId}/`)
    // You may want to redirect or remove the post from view
    post.value = null
  } catch (e) {
    console.error('Failed to delete post:', e)
  }
}

const deleteReplyHandler = async (replyId) => {
  try {
    await authAxios.delete(`/posts/${replyId}/`)
    replies.value = replies.value.filter(r => r.id !== replyId)
  } catch (e) {
    console.error('Failed to delete reply:', e)
  }
}

onMounted(async () => {
  try {
    const response = await authAxios.get(`/posts/${route.params.id}/`)
    post.value = response.data
    await fetchReplies()
  } catch (error) {
    console.error('Failed to load post:', error)
  } finally {
    loading.value = false
  }
})
</script>
