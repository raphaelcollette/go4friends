<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background);">
    <main class="flex-1 flex pt-24 px-6 space-x-8 max-w-7xl mx-auto w-full">
      
      <!-- Left: Activity Log -->
      <aside class="hidden md:flex flex-col w-1/3 max-w-xs space-y-6 sticky top-32">
        <div class="glossy-bg rounded-2xl shadow-lg p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 text-center">📝 Activity Log</h3>
          <div class="space-y-6">
            <div v-for="(activity, index) in activities" :key="index" class="flex flex-col">
              <div class="flex items-start space-x-3">
                <div class="w-3 h-3 bg-purple-500 rounded-full mt-1"></div>
                <div>
                  <p class="text-sm text-gray-700">{{ activity.description }}</p>
                  <p class="text-xs text-gray-400">{{ activity.time }}</p>
                </div>
              </div>
              <div v-if="index !== activities.length - 1" class="border-l-2 border-purple-300 h-6 ml-1"></div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Right: Main Feed -->
      <section class="flex-1 flex flex-col space-y-16">

        <!-- Welcome Card -->
        <div class="glossy-bg rounded-2xl shadow-lg p-8 w-full text-center">
          <h2 class="text-4xl font-extrabold text-gray-800 mb-4">Welcome to go4friends!</h2>
          <p class="text-gray-600 text-lg">Find friends, join clubs, attend events, and make your college experience unforgettable. 🚀</p>
        </div>

        <!-- Discover Events -->
        <section class="w-full">
          <h3 class="text-3xl font-bold text-gray-800 mb-6">🎉 Discover Upcoming Events</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <div 
              v-for="event in displayedEvents" 
              :key="event.id"
              class="glossy-bg p-6 rounded-2xl shadow-md hover:shadow-xl transition-all cursor-pointer flex flex-col items-center text-center"
            >
              <h4 class="text-xl font-bold text-gray-800 mb-2">{{ event.title }}</h4>
              <p class="text-gray-600 text-sm">{{ event.location || 'No location specified' }}</p>
            </div>
          </div>
        </section>

        <!-- Join Clubs -->
        <section class="w-full">
          <h3 class="text-3xl font-bold text-gray-800 mb-6">🏛️ Join Clubs & Communities</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            <RouterLink
              v-for="club in displayedClubs"
              :key="club.id"
              :to="`/clubs/${encodeURIComponent(club.name)}`"
              class="glossy-bg p-6 rounded-2xl shadow-md hover:shadow-xl transition-all cursor-pointer flex flex-col items-center text-center"
            >
              <h4 class="text-xl font-bold text-gray-800 mb-2">{{ club.name }}</h4>
              <p class="text-gray-600 text-sm">{{ club.description || 'No description provided.' }}</p>
            </RouterLink>
          </div>
        </section>

        <!-- Tour Video Placeholder -->
        <section class="w-full">
          <h3 class="text-3xl font-bold text-gray-800 mb-6">🎥 Take a Tour!</h3>
          <div class="glossy-bg rounded-2xl shadow-md p-6 flex flex-col items-center justify-center">
            <div class="w-full h-64 bg-gray-300 rounded-xl flex items-center justify-center text-gray-600 text-xl">
              🎥 Tour Video Coming Soon
            </div>
          </div>
        </section>

      </section>

    </main>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useEventStore } from '@/stores/events'
import { useClubStore } from '@/stores/club'

const eventStore = useEventStore()
const clubStore = useClubStore()

const activities = ref([
  { description: 'You joined the Chess Club.', time: '2 hours ago' },
  { description: 'You RSVP\'d to Open Mic Night.', time: 'Yesterday' },
  { description: 'You added "Photography" to your interests.', time: '2 days ago' },
  { description: 'You made 3 new friends!', time: 'Last week' },
])

const displayedEvents = computed(() => eventStore.events.slice(0, 3))
const displayedClubs = computed(() => clubStore.clubs.slice(0, 3))

onMounted(async () => {
  await eventStore.fetchEvents()
  await clubStore.fetchClubs()
})
</script>

