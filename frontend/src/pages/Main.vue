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

          <!-- Post Entry Card locked at top -->
          <div class="glossy-bg rounded-2xl shadow-lg p-6 mb-6 sticky top-0 bg-white/90 backdrop-blur-sm z-20">
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span class="text-white font-bold text-lg">{{ userInitials }}</span>
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
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 disabled:opacity-50 transition-all"
                  >
                    {{ isPosting ? 'Posting...' : 'Post' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Posts container with scroll -->
          <div 
            ref="postsContainer" 
            class="space-y-6 overflow-y-auto flex-grow scrollbar-hidden" 
            style="max-height: 100%;"
            @scroll="handleScroll"
          >
            <!-- Posts List -->
            <div
              v-for="post in filteredPosts"
              :key="post.id"
              class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 mb-6"
            >
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

            <div v-if="!loadingMore && !allLoaded" class="flex justify-center mt-4">
              <button
                @click="loadMorePosts"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
              >
                Load More
              </button>
            </div>
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
            <RouterLink to="/events" class="inline-block px-6 py-2 bg-white/80 text-gray-700 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
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
            <RouterLink to="/clubs" class="inline-block px-6 py-2 bg-white/80 text-gray-700 font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              Browse All Clubs
            </RouterLink>
          </div>
        </section>

      </aside>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
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

const displayedEvents = computed(() => (eventStore.events ?? []).slice(0, 3))
const displayedClubs = computed(() => (clubStore.clubs ?? []).slice(0, 3))

// Posts filtered by activeTab and paginated
const filteredPosts = computed(() => {
  const posts = postStore.posts ?? []
  let filtered = posts.filter(p => {
    if (p.club) return false
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
    // Reset pagination after new post
    postsPage.value = 1
    allLoaded.value = false
    await postStore.fetchPosts()
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

// Load more posts on clicking button
const loadMorePosts = () => {
  if (loadingMore.value || allLoaded.value) return
  loadingMore.value = true
  setTimeout(() => {
    postsPage.value++
    loadingMore.value = false
    // Check if we've loaded all posts
    const postsCount = (postStore.posts ?? []).filter(p => {
      if (p.club) return false
      if (activeTab.value === 'public') return !p.is_anonymous
      if (activeTab.value === 'anonymous') return p.is_anonymous
      return false
    }).length
    if (filteredPosts.value.length >= postsCount) {
      allLoaded.value = true
    }
  }, 600) // simulate load delay
}

const postsContainer = ref(null)

// Optional: Infinite scroll handler to trigger load more when near bottom
const handleScroll = (e) => {
  const el = e.target
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - 100) {
    loadMorePosts()
  }
}

// Reset pagination & allLoaded when tab changes
watch(activeTab, () => {
  postsPage.value = 1
  allLoaded.value = false
})

onMounted(async () => {
  await eventStore.fetchEvents()
  await clubStore.fetchClubs()
  await postStore.fetchPosts()
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
