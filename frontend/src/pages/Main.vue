<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 max-w-7xl mx-auto w-full gap-8" style="height: calc(100vh - 6rem);">

      <!-- Main Content - Posts Feed -->
      <section class="flex-1 flex flex-col h-full">

        <!-- Social Feed Section -->
        <section class="w-full flex flex-col flex-grow overflow-hidden">
          <div class="text-center mb-8 flex-shrink-0">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">📱 Campus Feed</h2>
            <p class="text-gray-600 text-lg">Stay connected with what's happening around campus</p>
          </div>

          <!-- Tabs -->
          <div class="flex justify-center space-x-4 mb-6 flex-shrink-0">
            <button
              @click="activeTab = 'public'"
              :class="activeTab === 'public' ? 'border-b-2 border-blue-600 font-semibold' : 'text-gray-600 hover:text-gray-800'"
              class="pb-2"
            >
              Public Posts
            </button>
            <button
              @click="activeTab = 'anonymous'"
              :class="activeTab === 'anonymous' ? 'border-b-2 border-blue-600 font-semibold' : 'text-gray-600 hover:text-gray-800'"
              class="pb-2"
            >
              Anonymous Posts
            </button>
          </div>

          <div
            ref="postsContainer"
            class="space-y-6 overflow-y-auto scrollbar-hidden"
            style="height: 100%;"
            @scroll.passive="handleScroll"
          >
            <!-- New Post Composer -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6 mb-6 flex-shrink-0">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 flex-shrink-0">
                  <div
                    v-if="activeTab === 'anonymous'"
                    class="w-12 h-12 rounded-full flex items-center justify-center"
                    :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
                  >
                    <span class="text-white font-bold text-lg">AN</span>
                  </div>

                  <img
                    v-else-if="currentUser && currentUser.profile_picture_url"
                    :src="currentUser.profile_picture_url"
                    alt="Profile Picture"
                    class="w-12 h-12 rounded-full object-cover border-2 border-purple-400"
                  />

                  <div
                    v-else
                    class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg"
                    :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
                  >
                    <span>{{ userInitials }}</span>
                  </div>
                </div>
                <div class="flex-1">
                  <textarea
                    v-model="newPostContent"
                    placeholder="What's happening?"
                    rows="3"
                    class="w-full bg-white/70 rounded-xl p-3 text-gray-800 focus:outline-none resize-none"
                  ></textarea>
                  <div class="flex items-center justify-between mt-2">
                    <button
                      :disabled="isPosting || newPostContent.trim() === ''"
                      @click="submitPost"
                      class="btn px-4 py-2 rounded-lg shadow-md disabled:opacity-50 transition-all"
                    >
                      {{ isPosting ? 'Posting...' : 'Post' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Skeleton Loader -->
            <template v-if="loadingPosts">
              <div
                v-for="n in 5"
                :key="n"
                class="glossy-bg rounded-2xl shadow-lg p-6 mb-6 animate-pulse"
              >
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 rounded-full bg-gray-300"></div>
                  <div class="flex-1 space-y-3 py-1">
                    <div class="h-4 bg-gray-300 rounded w-1/3"></div>
                    <div class="space-y-2">
                      <div class="h-4 bg-gray-300 rounded"></div>
                      <div class="h-4 bg-gray-300 rounded w-5/6"></div>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <!-- Posts List -->
            <template v-else>
              <div
                v-for="post in filteredPosts"
                :key="post.id"
                class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 mb-6"
              >
                <div class="flex items-start space-x-4">
                  <RouterLink :to="`/profile/${post.username}`" class="flex-shrink-0">
                    <div v-if="post.user && post.user.profile_picture_url">
                      <img
                        :src="post.user.profile_picture_url"
                        alt="Profile Picture"
                        class="w-12 h-12 rounded-full object-cover border-2 border-purple-400"
                      />
                    </div>
                    <div
                      v-else
                      class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg"
                      :style="{ backgroundColor: 'var(--btn-primary, #6366f1)' }"
                    >
                      {{ post.authorInitials }}
                    </div>
                  </RouterLink>
                  <div class="flex-1">
                    <RouterLink
                      :to="`/posts/${post.id}`"
                      class="block"
                    >
                      <div class="flex items-center space-x-2 mb-2">
                        <RouterLink
                          :to="`/profile/${post.username}`"
                          class="flex items-center space-x-2 mb-2 hover:underline"
                        >
                          <h4 class="font-bold text-gray-800">{{ post.authorName }}</h4>
                          <span class="text-gray-500 text-sm">@{{ post.username }}</span>
                          <span class="text-gray-400 text-sm">·</span>
                          <span class="text-gray-500 text-sm">{{ post.timeAgo }}</span>
                        </RouterLink>
                      </div>
                      <p class="text-gray-700 mb-3 leading-relaxed">{{ post.content }}</p>
                    </RouterLink>

                    <div class="flex items-center space-x-6 text-gray-500 mt-2">
                      <button
                        class="flex items-center space-x-2 hover:text-blue-500 transition-colors"
                        @click.stop
                      >
                        <span>💬</span>
                        <span class="text-sm">{{ post.commentCount }}</span>
                      </button>

                      <button
                        v-if="!post.hasLiked"
                        class="flex items-center space-x-2 hover:text-red-500 transition-colors"
                        @click.stop="likePost(post.id)"
                      >
                        <span>❤️</span>
                        <span class="text-sm">{{ post.likeCount }}</span>
                      </button>
                      <button
                        v-else
                        class="flex items-center space-x-2 text-red-500 transition-colors"
                        @click.stop="unlikePost(post.id)"
                      >
                        <span>🗑️❤️</span>
                        <span class="text-sm">{{ post.likeCount }}</span>
                      </button>

                      <button
                        v-if="!post.hasReposted"
                        class="flex items-center space-x-2 hover:text-green-500 transition-colors"
                        @click.stop="repostPost(post.id)"
                      >
                        <span>🔁</span>
                        <span class="text-sm">{{ post.repostCount }}</span>
                      </button>
                      <button
                        v-else
                        class="flex items-center space-x-2 text-green-600 transition-colors"
                        @click.stop="undoRepostPost(post.id)"
                      >
                        <span>🗑️🔁</span>
                        <span class="text-sm">{{ post.repostCount }}</span>
                      </button>

                      <button
                        v-if="canDeletePost(post)"
                        @click.stop="deletePostHandler(post.id)"
                        class="ml-4 text-red-600 hover:text-red-800 transition-colors"
                        title="Delete post"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <div v-if="loadingMore" class="text-center text-gray-500 mt-4 select-none">Loading...</div>
            <div v-if="allLoaded && filteredPosts.length" class="text-center text-gray-500 mt-4 select-none">No more posts</div>
          </div>
        </section>

      </section>

      <!-- Sidebar - Events and Clubs -->
      <aside class="w-80 flex-shrink-0 space-y-8 overflow-auto scrollbar-hidden" style="max-height: calc(100vh - 6rem);">
        <!-- Discover Events -->
        <section class="w-full">
          <div class="text-center mb-6">
            <h3 class="text-2xl font-bold text-gray-800 mb-2">🎉 Upcoming Events</h3>
            <p class="text-gray-600 text-sm">Don't miss out on campus events</p>
          </div>

          <div v-if="displayedEvents.length > 0" class="space-y-4">
            <div
              v-for="event in displayedEvents"
              :key="event.id"
              class="glossy-bg p-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer group"
            >
              <div class="flex items-start space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-sm">🎉</span>
                </div>
                <div class="flex-1">
                  <h4 class="text-sm font-bold text-gray-800 mb-1">{{ event.title }}</h4>
                  <p class="text-gray-600 text-xs flex items-center">
                    <span class="mr-1">📍</span>
                    {{ event.location || 'No location specified' }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="glossy-bg rounded-xl shadow-lg p-6 text-center">
            <div class="text-3xl mb-2">🎭</div>
            <h4 class="text-lg font-bold text-gray-800 mb-1">No Events Yet</h4>
            <p class="text-gray-600 text-sm">Check back soon!</p>
          </div>

          <div class="text-center mt-4">
            <RouterLink
              to="/events"
              class="inline-block px-6 py-2 bg-white/80 text-gray-700 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              View All Events
            </RouterLink>
          </div>
        </section>

        <!-- Join Clubs -->
        <section class="w-full">
          <div class="text-center mb-6">
            <h3 class="text-2xl font-bold text-gray-800 mb-2">🏛️ Join Clubs</h3>
            <p class="text-gray-600 text-sm">Connect with like-minded students</p>
          </div>

          <div v-if="displayedClubs.length > 0" class="space-y-4">
            <RouterLink
              v-for="club in displayedClubs"
              :key="club.id"
              :to="`/clubs/${encodeURIComponent(club.name)}`"
              class="glossy-bg p-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer group block"
            >
              <div class="flex items-start space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-sm">🏛️</span>
                </div>
                <div class="flex-1">
                  <h4 class="text-sm font-bold text-gray-800 mb-1">{{ club.name }}</h4>
                  <p class="text-gray-600 text-xs leading-relaxed line-clamp-2">{{ club.description || 'No description provided.' }}</p>
                </div>
              </div>
            </RouterLink>
          </div>

          <div v-else class="glossy-bg rounded-xl shadow-lg p-6 text-center">
            <div class="text-3xl mb-2">🏛️</div>
            <h4 class="text-lg font-bold text-gray-800 mb-1">No Clubs Yet</h4>
            <p class="text-gray-600 text-sm">Be the first to create one!</p>
          </div>

          <div class="text-center mt-4">
            <RouterLink
              to="/clubs"
              class="inline-block px-6 py-2 bg-white/80 text-gray-700 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              Browse All Clubs
            </RouterLink>
          </div>
        </section>
      </aside>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useEventStore } from '@/stores/events'
import { useClubStore } from '@/stores/club'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/user'
import { useToast } from 'vue-toastification'

const eventStore = useEventStore()
const clubStore = useClubStore()
const postStore = usePostStore()
const userStore = useUserStore()
const toast = useToast()

const newPostContent = ref('')
const isPosting = ref(false)
const activeTab = ref('public') // 'public' or 'anonymous'
const loadingMore = ref(false)
const allLoaded = ref(false)
const postsPage = ref(1)
const postsPerPage = 10
const loadingPosts = ref(true)

const displayedEvents = computed(() => (eventStore.events ?? []).slice(0, 3))
const displayedClubs = computed(() => (clubStore.clubs ?? []).slice(0, 3))

const currentUser = userStore.currentUser

const filteredPosts = computed(() => {
  const posts = postStore.posts ?? []
  let filtered = posts.filter(p => {
    if (p.club) return false
    if (p.parent) return false
    if (activeTab.value === 'public') return !p.is_anonymous
    if (activeTab.value === 'anonymous') return p.is_anonymous
    return false
  })
  return filtered.slice(0, postsPage.value * postsPerPage)
})

const submitPost = async () => {
  if (newPostContent.value.trim() === '') return
  isPosting.value = true
  try {
    const anonymous = activeTab.value === 'anonymous'
    await postStore.createPost(newPostContent.value, anonymous)
    newPostContent.value = ''
    postsPage.value = 1
    allLoaded.value = false
    loadingPosts.value = true
    await postStore.fetchPosts()
    loadingPosts.value = false
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to post.'
    toast.error(msg)
  } finally {
    isPosting.value = false
  }
}

const userInitials = computed(() => {
  const user = userStore.currentUser
  if (!user) return 'U'
  const names = user.full_name?.split(' ') || []
  return names.slice(0, 2).map(n => n[0]?.toUpperCase()).join('') || user.username?.[0]?.toUpperCase() || 'U'
})

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

const loadMorePosts = () => {
  if (loadingMore.value || allLoaded.value) return
  loadingMore.value = true
  setTimeout(() => {
    postsPage.value++
    loadingMore.value = false
    const postsCount = (postStore.posts ?? []).filter(p => {
      if (p.club) return false
      if (activeTab.value === 'public') return !p.is_anonymous
      if (activeTab.value === 'anonymous') return p.is_anonymous
      return false
    }).length
    if (filteredPosts.value.length >= postsCount) {
      allLoaded.value = true
    }
  }, 600)
}

const postsContainer = ref(null)

const handleScroll = () => {
  const el = postsContainer.value
  if (!el) return
  const nearBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 50
  if (nearBottom && !loadingMore.value && !allLoaded.value) {
    loadMorePosts()
  }
}

const canDeletePost = (post) => {
  if (!userStore.currentUser) return false

  const currentUsername = userStore.currentUser.username

  if (post.club) {
    const membership = clubStore.memberships?.find(m => m.club.id === post.club.id)
    return membership && ['moderator', 'admin'].includes(membership.role)
  }

  return post.author_username === currentUsername
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

watch(activeTab, async () => {
  postsPage.value = 1
  allLoaded.value = false
  loadingPosts.value = true
  await postStore.fetchPosts()
  loadingPosts.value = false
  await nextTick()
  handleScroll()
})

onMounted(async () => {
  await eventStore.fetchEvents()
  await clubStore.fetchClubs()
  loadingPosts.value = true
  await postStore.fetchPosts()
  loadingPosts.value = false
  requestAnimationFrame(() => handleScroll())
})
</script>

<style>
/* Hide scrollbar */
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
.scrollbar-hidden {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>
