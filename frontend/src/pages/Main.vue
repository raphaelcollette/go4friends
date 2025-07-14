<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 max-w-6xl mx-auto w-full">
      
      <!-- Main Content -->
      <section class="flex-1 flex flex-col space-y-20">

        <!-- Welcome Hero Section -->
        <div class="glossy-bg rounded-3xl shadow-xl p-12 w-full text-center relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10 rounded-3xl"></div>
          <div class="relative z-10">
            <h1 class="text-5xl font-extrabold text-gray-800 mb-6 leading-tight">
              Welcome to <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600">go4friends!</span>
            </h1>
            <p class="text-gray-600 text-xl max-w-3xl mx-auto leading-relaxed">
              Find friends, join clubs, attend events, and make your college experience unforgettable. 🚀
            </p>
            <div class="mt-8 flex justify-center space-x-4">
              <button class="px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                Get Started
              </button>
              <button class="px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                Learn More
              </button>
            </div>
          </div>
        </div>

        <!-- Stats Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="glossy-bg rounded-2xl shadow-lg p-8 text-center">
            <div class="text-4xl font-bold text-purple-600 mb-2">150+</div>
            <div class="text-gray-600 font-medium">Active Clubs</div>
          </div>
          <div class="glossy-bg rounded-2xl shadow-lg p-8 text-center">
            <div class="text-4xl font-bold text-blue-600 mb-2">500+</div>
            <div class="text-gray-600 font-medium">Events This Month</div>
          </div>
          <div class="glossy-bg rounded-2xl shadow-lg p-8 text-center">
            <div class="text-4xl font-bold text-green-600 mb-2">2.5K+</div>
            <div class="text-gray-600 font-medium">Students Connected</div>
          </div>
        </div>

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
            <button class="px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              View All Events
            </button>
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
            <button class="px-8 py-3 bg-white/80 text-gray-700 font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              Browse All Clubs
            </button>
          </div>
        </section>

        <!-- Tour Video Section -->
        <section class="w-full">
          <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-800 mb-4">🎥 Take a Tour!</h2>
            <p class="text-gray-600 text-lg">See how go4friends can transform your college experience</p>
          </div>
          
          <div class="glossy-bg rounded-3xl shadow-xl p-8">
            <div class="w-full h-80 bg-gradient-to-br from-gray-200 to-gray-300 rounded-2xl flex flex-col items-center justify-center text-gray-600 relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10"></div>
              <div class="relative z-10 text-center">
                <div class="w-24 h-24 bg-white/80 rounded-full flex items-center justify-center mb-6 mx-auto shadow-lg">
                  <span class="text-4xl">▶️</span>
                </div>
                <h3 class="text-2xl font-bold mb-2">Tour Video Coming Soon</h3>
                <p class="text-gray-500">Get ready for an amazing preview of campus life!</p>
              </div>
            </div>
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

