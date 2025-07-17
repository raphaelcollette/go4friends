<template> 
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex pt-24 px-6 max-w-7xl mx-auto w-full gap-8">

      <!-- Posts Section (Left) -->
      <section class="flex-1 flex flex-col">
        <div v-if="loadingPosts" class="text-gray-600 text-lg">Loading posts...</div>
        <div v-else-if="user?.private" class="text-gray-600 text-lg">Posts are hidden due to private profile.</div>
        <div v-else>
          <div
            v-for="post in filteredPosts"
            :key="post.id"
            class="glossy-bg rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 mb-6 cursor-pointer"
          >
            <router-link :to="`/posts/${post.id}`" class="block text-inherit no-underline px-6 pt-6">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">{{ post.authorInitials }}</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-2">
                    <h4 class="font-bold text-gray-800">{{ post.authorName }}</h4>
                    <span class="text-gray-500 text-sm">@{{ post.username }}</span>
                    <span class="text-gray-400 text-sm">·</span>
                    <span class="text-gray-500 text-sm">{{ post.timeAgo }}</span>
                  </div>
                  <p class="text-gray-700 mb-3 leading-relaxed">{{ post.content }}</p>
                </div>
              </div>
            </router-link>

            <div class="flex items-center space-x-6 text-gray-500 px-6 pb-4">
              <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors" disabled>
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
          </div>
        </div>
      </section>

      <!-- Profile Section (Right) -->
      <section class="w-80 flex-shrink-0">
        <div v-if="loading" class="text-gray-600 text-lg">Loading profile...</div>

        <div v-else-if="user?.private" class="glossy-bg rounded-2xl shadow-md p-6 text-center">
          <h2 class="text-2xl font-bold text-gray-800">🔒 Private Profile</h2>
          <p class="text-gray-600 mt-2">This user's profile is private and only visible to friends.</p>
        </div>

        <div v-else-if="!user" class="glossy-bg rounded-2xl shadow-md p-6 text-center">
          <h2 class="text-2xl font-bold text-gray-800">❌ User Not Found</h2>
          <p class="text-gray-600 mt-2">We couldn't find anyone with that username.</p>
        </div>

        <div v-else class="glossy-bg rounded-2xl shadow-lg p-8 text-center">
          <div class="flex justify-center">
            <img
              v-if="user.profile_picture"
              :src="user.profile_picture"
              alt="Profile Picture"
              class="w-28 h-28 rounded-full object-cover border-4"
              :style="{ borderColor: 'var(--btn-primary, #6366f1)' }"
            />
            <div v-else class="w-28 h-28 rounded-full flex items-center justify-center text-4xl text-white"
              :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }">
              {{ user.username.charAt(0).toUpperCase() }}
            </div>
          </div>

          <h1 class="text-3xl font-bold text-gray-800 mt-6">{{ user.full_name || user.username }}</h1>
          <p class="text-gray-600 mt-2">@{{ user.username }}</p>

          <p v-if="user.bio" class="mt-4 text-gray-700 italic">{{ user.bio }}</p>
          <p v-if="user.location" class="text-gray-500 text-sm mt-2">📍 {{ user.location }}</p>

          <!-- Friend Actions -->
          <div class="mt-6" v-if="!isCurrentUser">
            <button v-if="user.is_friend" @click="removeFriend" class="redbtn">Unfriend</button>
            <button v-else-if="user.friend_request_sent" class="btn" disabled>Request Sent</button>
            <button v-else @click="sendFriendRequest" class="btn">+ Add Friend</button>

            <div class="mt-4">
              <button @click="startOrNavigateToThread" class="btn">💬 Message</button>
            </div>
          </div>

          <!-- Clubs -->
          <div v-if="user.clubs?.length" class="mt-8">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Clubs</h2>
            <div class="flex flex-wrap justify-center gap-2">
              <router-link
                v-for="club in user.clubs"
                :key="club.id"
                :to="`/clubs/${encodeURIComponent(club.name)}`"
                class="bg-purple-100 text-purple-700 text-sm font-semibold px-3 py-1 rounded-full hover:bg-purple-200 transition"
              >
                {{ club.name }}
              </router-link>
            </div>
          </div>

          <p class="text-gray-600 mt-4 text-sm">👥 Friends: {{ friendCount !== null ? friendCount : 'Loading...' }}</p>

          <!-- Interests -->
          <div v-if="user.interests?.length" class="mt-8">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Interests</h2>
            <div class="flex flex-wrap justify-center gap-2">
              <span
                v-for="(interest, idx) in user.interests"
                :key="idx"
                class="text-sm font-semibold px-3 py-1 rounded-full"
                :style="{
                  backgroundColor: 'var(--btn-secondary, #a5b4fc)',
                  color: 'var(--btn-primary, #6366f1)',
                }"
              >
                {{ interest }}
              </span>
            </div>
          </div>

          <p v-if="user.major" class="mt-2 text-gray-600 text-sm">🎓 Major: {{ user.major }}</p>
          <p v-if="user.graduation_year" class="text-gray-600 text-sm">🎓 Class of {{ user.graduation_year }}</p>

          <div class="mt-6 flex justify-center space-x-4">
            <router-link to="/friends" class="btn">Back to Friends</router-link>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'
import { usePostStore } from '@/stores/posts'
import { useFriendStore } from '@/stores/friend'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const userStore = useUserStore()
const postStore = usePostStore()
const friendStore = useFriendStore()

const user = ref(null)
const loading = ref(true)
const loadingPosts = ref(true)

const friendCount = ref(null)

const isCurrentUser = computed(() => {
  return userStore.currentUser && user.value && userStore.currentUser.username === user.value.username
})

const fetchUser = async () => {
  loading.value = true
  const username = route.params.username
  const now = Date.now()
  const oneMinute = 60 * 1000

  try {
    const cached = userStore.profileCache[username]
    if (cached && (now - cached.lastFetched) < oneMinute) {
      user.value = cached.data
    } else {
      const res = await authAxios.get(`/users/profile/${username}/`)
      user.value = res.data

      userStore.profileCache[username] = {
        data: res.data,
        lastFetched: now
      }

      if (userStore.currentUser && username === userStore.currentUser.username) {
        userStore.currentUser = res.data
        localStorage.setItem('currentUser', JSON.stringify(res.data))
      }
    }
  } catch (error) {
    if (error.response?.status === 403) {
      user.value = { private: true }
    } else {
      toast.error('Failed to load user profile.')
      user.value = null
    }
  } finally {
    loading.value = false
  }
}

const fetchPosts = async () => {
  loadingPosts.value = true
  try {
    await postStore.fetchUserPosts(route.params.username)
  } catch {
    toast.error('Failed to load posts.')
  } finally {
    loadingPosts.value = false
  }
}

const fetchFriendCount = async (username) => {
  const oneMinute = 60 * 1000
  const now = Date.now()

  if (
    friendStore.friendCountCache?.[username] &&
    now - friendStore.friendCountCache[username].lastFetched < oneMinute
  ) {
    friendCount.value = friendStore.friendCountCache[username].count
    return
  }

  try {
    const res = await authAxios.get(`/friends/${encodeURIComponent(username)}/count/`)
    const count = res.data.friends_count

    if (!friendStore.friendCountCache) friendStore.friendCountCache = {}

    friendStore.friendCountCache[username] = {
      count,
      lastFetched: now,
    }

    friendCount.value = count
  } catch {
    toast.error('Failed to load friends count.')
    friendCount.value = null
  }
}

const filteredPosts = computed(() => {
  if (!user.value || user.value.private) return []
  return postStore.userPosts.filter(post => !post.parent)
})

const sendFriendRequest = async () => {
  try {
    await authAxios.post('/friends/send/', { to_username: user.value.username })
    toast.success('Friend request sent!')
    user.value.friend_request_sent = true
  } catch {
    toast.error('Failed to send friend request.')
  }
}

const removeFriend = async () => {
  try {
    await authAxios.post('/friends/remove/', { username: user.value.username })
    toast.success('Friend removed.')
    user.value.is_friend = false
  } catch {
    toast.error('Failed to remove friend.')
  }
}

const startOrNavigateToThread = async () => {
  try {
    const res = await authAxios.post('/messages/threads/start-private/', {
      username: user.value.username,
    })
    router.push(`/messages?thread=${res.data.thread_id}`)
  } catch {
    toast.error('Could not start chat.')
  }
}

const likePost = async (postId) => {
  try {
    await postStore.likePost(postId)
  } catch (e) {
    console.error(e)
  }
}

const unlikePost = async (postId) => {
  try {
    await postStore.unlikePost(postId)
  } catch (e) {
    console.error(e)
  }
}

const repostPost = async (postId) => {
  try {
    await postStore.repostPost(postId)
  } catch (e) {
    console.error(e)
  }
}

const undoRepostPost = async (postId) => {
  try {
    await postStore.undoRepostPost(postId)
  } catch (e) {
    console.error(e)
  }
}

const deletePostHandler = async (postId) => {
  try {
    await postStore.deletePost(postId)
    toast.success('Post deleted')
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to delete post'
    toast.error(msg)
  }
}

const canDeletePost = (post) => {
  if (!userStore.currentUser) return false

  const currentUsername = userStore.currentUser.username

  if (post.club) {
    const membership = clubStore.memberships?.find(m => m.club.id === post.club.id)
    return membership && ['moderator', 'admin'].includes(membership.role)
  }

  return post.username === currentUsername
}

onMounted(async () => {
  await fetchUser()
  await fetchPosts()
  if (user.value?.username) {
    await fetchFriendCount(user.value.username)
  }
})

watch(() => route.params.username, async (newUsername) => {
  await fetchUser()
  await fetchPosts()
  if (newUsername) {
    await fetchFriendCount(newUsername)
  }
})
</script>
