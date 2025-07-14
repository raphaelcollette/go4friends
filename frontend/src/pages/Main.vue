<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 max-w-6xl mx-auto w-full">
      
      <!-- Main Content -->
      <section class="flex-1 flex flex-col space-y-20">

        <!-- Social Feed Section -->
        <section class="w-full">
          <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">📱 Campus Feed</h2>
            <p class="text-gray-600 text-lg">Stay connected with what's happening around campus</p>
          </div>
          
          <div class="space-y-6">
            <!-- Post 1 -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">JS</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-2">
                    <h4 class="font-bold text-gray-800">John Smith</h4>
                    <span class="text-gray-500 text-sm">@johnsmith</span>
                    <span class="text-gray-400 text-sm">·</span>
                    <span class="text-gray-500 text-sm">2h</span>
                  </div>
                  <p class="text-gray-700 mb-3 leading-relaxed">
                    Just finished my first week at the Computer Science Club! 💻 The projects we're working on are incredible. Can't wait to show you all what we build next! #coding #college
                  </p>
                  <div class="flex items-center space-x-6 text-gray-500">
                    <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                      <span>💬</span>
                      <span class="text-sm">12</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-green-500 transition-colors">
                      <span>🔁</span>
                      <span class="text-sm">3</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-red-500 transition-colors">
                      <span>❤️</span>
                      <span class="text-sm">24</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Post 2 -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">EM</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-2">
                    <h4 class="font-bold text-gray-800">Emily Martinez</h4>
                    <span class="text-gray-500 text-sm">@emartinez</span>
                    <span class="text-gray-400 text-sm">·</span>
                    <span class="text-gray-500 text-sm">4h</span>
                  </div>
                  <p class="text-gray-700 mb-3 leading-relaxed">
                    The campus coffee shop is serving pumpkin spice lattes again! ☕🍂 Perfect fuel for those late-night study sessions. Who else is excited for fall semester?
                  </p>
                  <div class="w-full h-48 bg-gradient-to-br from-orange-200 to-amber-200 rounded-xl flex items-center justify-center mb-3">
                    <span class="text-4xl">☕</span>
                  </div>
                  <div class="flex items-center space-x-6 text-gray-500">
                    <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                      <span>💬</span>
                      <span class="text-sm">8</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-green-500 transition-colors">
                      <span>🔁</span>
                      <span class="text-sm">5</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-red-500 transition-colors">
                      <span>❤️</span>
                      <span class="text-sm">31</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Post 3 -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-pink-500 to-rose-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">AC</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-2">
                    <h4 class="font-bold text-gray-800">Alex Chen</h4>
                    <span class="text-gray-500 text-sm">@alexchen</span>
                    <span class="text-gray-400 text-sm">·</span>
                    <span class="text-gray-500 text-sm">6h</span>
                  </div>
                  <p class="text-gray-700 mb-3 leading-relaxed">
                    Looking for study buddies for tomorrow's chemistry exam! 🧪 Anyone else procrastinating and need some motivation? Let's conquer this together! 
                  </p>
                  <div class="flex items-center space-x-6 text-gray-500">
                    <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                      <span>💬</span>
                      <span class="text-sm">15</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-green-500 transition-colors">
                      <span>🔁</span>
                      <span class="text-sm">7</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-red-500 transition-colors">
                      <span>❤️</span>
                      <span class="text-sm">18</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Post 4 -->
            <div class="glossy-bg rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-white font-bold text-lg">MJ</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-2">
                    <h4 class="font-bold text-gray-800">Maya Johnson</h4>
                    <span class="text-gray-500 text-sm">@mayaj</span>
                    <span class="text-gray-400 text-sm">·</span>
                    <span class="text-gray-500 text-sm">1d</span>
                  </div>
                  <p class="text-gray-700 mb-3 leading-relaxed">
                    Just got accepted into the Photography Club! 📸 Can't wait to explore campus and capture all the beautiful moments. First assignment: sunrise over the quad tomorrow morning!
                  </p>
                  <div class="flex items-center space-x-6 text-gray-500">
                    <button class="flex items-center space-x-2 hover:text-blue-500 transition-colors">
                      <span>💬</span>
                      <span class="text-sm">9</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-green-500 transition-colors">
                      <span>🔁</span>
                      <span class="text-sm">2</span>
                    </button>
                    <button class="flex items-center space-x-2 hover:text-red-500 transition-colors">
                      <span>❤️</span>
                      <span class="text-sm">26</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Load More Button -->
            <div class="text-center pt-6">
              <button class="px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                Load More Posts
              </button>
            </div>
          </div>
        </section>

        <!-- Discover Events -->
        <section class="w-full">
          <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">🎉 Discover Upcoming Events</h2>
            <p class="text-gray-600 text-lg">Don't miss out on the hottest events happening around campus</p>
          </div>
          
          <div v-if="displayedEvents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div 
              v-for="event in displayedEvents" 
              :key="event.id"
              class="glossy-bg p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer flex flex-col items-center text-center group transform hover:scale-105"
            >
              <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <span class="text-2xl">🎉</span>
              </div>
              <h4 class="text-xl font-bold text-gray-800 mb-3">{{ event.title }}</h4>
              <p class="text-gray-600 text-sm flex items-center">
                <span class="mr-2">📍</span>
                {{ event.location || 'No location specified' }}
              </p>
              <button class="mt-4 px-6 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-medium rounded-lg hover:shadow-lg transition-all opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0">
                View Details
              </button>
            </div>
          </div>

          <div v-else class="glossy-bg rounded-2xl shadow-lg p-12 text-center">
            <div class="text-6xl mb-4">🎭</div>
            <h3 class="text-2xl font-bold text-gray-800 mb-2">No Events Yet</h3>
            <p class="text-gray-600">Check back soon for exciting upcoming events!</p>
          </div>

          <div class="text-center mt-12">
            <RouterLink to="/events" class="inline-block px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              View All Events
            </RouterLink>
          </div>
        </section>

        <!-- Join Clubs -->
        <section class="w-full">
          <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">🏛️ Join Clubs & Communities</h2>
            <p class="text-gray-600 text-lg">Connect with like-minded students and pursue your passions</p>
          </div>
          
          <div v-if="displayedClubs.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <RouterLink
              v-for="club in displayedClubs"
              :key="club.id"
              :to="`/clubs/${encodeURIComponent(club.name)}`"
              class="glossy-bg p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer flex flex-col items-center text-center group transform hover:scale-105"
            >
              <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <span class="text-2xl">🏛️</span>
              </div>
              <h4 class="text-xl font-bold text-gray-800 mb-3">{{ club.name }}</h4>
              <p class="text-gray-600 text-sm leading-relaxed">{{ club.description || 'No description provided.' }}</p>
              <button class="mt-4 px-6 py-2 bg-gradient-to-r from-green-500 to-teal-500 text-white font-medium rounded-lg hover:shadow-lg transition-all opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0">
                Join Club
              </button>
            </RouterLink>
          </div>

          <div v-else class="glossy-bg rounded-2xl shadow-lg p-12 text-center">
            <div class="text-6xl mb-4">🏛️</div>
            <h3 class="text-2xl font-bold text-gray-800 mb-2">No Clubs Yet</h3>
            <p class="text-gray-600">Be the first to create or join a club!</p>
          </div>

          <div class="text-center mt-12">
            <RouterLink to="/clubs" class="inline-block px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              Browse All Clubs
            </RouterLink>
          </div>
        </section>

      </section>

    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useEventStore } from '@/stores/events'
import { useClubStore } from '@/stores/club'

const eventStore = useEventStore()
const clubStore = useClubStore()

const displayedEvents = computed(() => eventStore.events.slice(0, 3))
const displayedClubs = computed(() => clubStore.clubs.slice(0, 3))

onMounted(async () => {
  await eventStore.fetchEvents()
  await clubStore.fetchClubs()
})
</script>

