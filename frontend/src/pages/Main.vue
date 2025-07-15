<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 max-w-7xl mx-auto w-full gap-8">
      
      <!-- Main Content - Posts Feed -->
      <section class="flex-1 flex flex-col">

        <!-- Social Feed Section -->
        <section class="w-full">
          <div class="text-center mb-8">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">📱 Campus Feed</h2>
            <p class="text-gray-600 text-lg">Stay connected with what's happening around campus</p>
          </div>
          
          <div class="space-y-6">
            <!-- New Post Composer -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">
                    {{ userInitials }}
                  </span>
                </div>
                <div class="flex-1">
                  <textarea
                    v-model="newPostContent"
                    placeholder="What's happening?"
                    rows="3"
                    class="w-full bg-white/70 rounded-xl p-3 text-gray-800 focus:outline-none resize-none"
                  ></textarea>
                  <div class="flex items-center justify-between mt-2">
                    <label class="inline-flex items-center space-x-2 text-gray-700 select-none">
                      <input type="checkbox" v-model="isAnonymous" />
                      <span>Post anonymously</span>
                    </label>
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
            <!-- Real Posts -->
            <div
              v-for="post in filteredPosts"
              :key="post.id"
              class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300"
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
                    <!-- Like Button -->
                    <button
                      v-if="!post.hasLiked"
                      class="flex items-center space-x-2 hover:text-red-500 transition-colors"
                      @click="likePost(post.id)"
                    >
                      <span>❤️</span>
                      <span class="text-sm">{{ post.likeCount }}</span>
                    </button>
                    <!-- Unlike Button -->
                    <button
                      v-else
                      class="flex items-center space-x-2 text-red-500 transition-colors"
                      @click="unlikePost(post.id)"
                    >
                      <span>🗑️❤️</span>
                      <span class="text-sm">{{ post.likeCount }}</span>
                    </button>

                    <!-- Repost Button -->
                    <button
                      v-if="!post.hasReposted"
                      class="flex items-center space-x-2 hover:text-green-500 transition-colors"
                      @click="repostPost(post.id)"
                    >
                      <span>🔁</span>
                      <span class="text-sm">{{ post.repostCount }}</span>
                    </button>
                    <!-- Undo Repost Button -->
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
           
          </div>
        </section>

      </section>

      <!-- Sidebar - Events and Clubs -->
      <aside class="w-80 flex-shrink-0 space-y-8">
        
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
import { ref, onMounted, computed } from 'vue'
import { useEventStore } from '@/stores/events'
import { useClubStore } from '@/stores/club'
import { usePostStore } from '@/stores/posts'
import { useUserStore } from '@/stores/user'

const eventStore = useEventStore()
const clubStore = useClubStore()
const postStore = usePostStore()
const userStore = useUserStore()

const displayedEvents = computed(() => eventStore.events.slice(0, 3))
const displayedClubs = computed(() => clubStore.clubs.slice(0, 3))

const newPostContent = ref('')
const isAnonymous = ref(false)
const isPosting = ref(false)

// Filter out posts with club assigned (exclude club posts)
const filteredPosts = computed(() => postStore.posts.filter(p => !p.club))

const submitPost = async () => {
  if (newPostContent.value.trim() === '') return
  isPosting.value = true
  try {
    await postStore.createPost(newPostContent.value, isAnonymous.value)
    newPostContent.value = ''
    isAnonymous.value = false
  } catch (e) {
    console.error(e)
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

onMounted(async () => {
  await eventStore.fetchEvents()
  await clubStore.fetchClubs()
  await postStore.fetchPosts()
})
</script>