<template>
    <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover;">
      <main class="flex-1 flex flex-col items-center pt-24 px-6">
  
        <!-- Loading -->
        <div v-if="loading" class="text-gray-600 text-lg">Loading event...</div>
  
        <!-- Event Not Found -->
        <div v-else-if="!event" class="glossy-bg rounded-2xl shadow-md p-6 max-w-md w-full text-center">
          <h2 class="text-2xl font-bold text-gray-800">❌ Event Not Found</h2>
          <p class="text-gray-600 mt-2">This event doesn't exist or was deleted.</p>
        </div>
  
        <!-- Event Card -->
        <div v-else class="glossy-bg rounded-2xl shadow-lg p-8 max-w-2xl w-full space-y-6 text-center">
          <h1 class="text-3xl font-extrabold text-gray-800">{{ event.title }}</h1>
  
          <p class="text-sm text-gray-500">{{ formatDate(event.date) }}</p>
          <p class="text-gray-600">{{ event.location || 'No location provided' }}</p>
  
          <img v-if="event.image" :src="event.image" alt="Event Image" class="rounded-xl w-full h-64 object-cover mt-4" />
  
          <p class="mt-4 text-gray-700 whitespace-pre-line">{{ event.description || 'No description provided.' }}</p>
  
          <!-- Attendees -->
          <div v-if="attendees.length" class="mt-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">👥 Attendees</h2>
            <div class="flex flex-wrap justify-center gap-3">
              <RouterLink
                v-for="user in attendees"
                :key="user.id"
                :to="`/profile/${user.username}`"
                class="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold hover:bg-purple-200 transition-all"
              >
                {{ user.full_name || user.username }}
              </RouterLink>
            </div>
          </div>
  
          <div v-else class="text-gray-400 text-sm">
            No attendees yet.
          </div>
  
          <div class="mt-8">
            <RouterLink to="/events" class="btn">⬅️ Back to Events</RouterLink>
          </div>
        </div>
  
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import { authAxios } from '@/utils/axios'
  import { useToast } from 'vue-toastification'
  import { useEventStore } from '@/stores/events'
  
  const route = useRoute()
  const toast = useToast()
  const eventStore = useEventStore()
  
  const event = ref(null)
  const attendees = ref([])
  const loading = ref(true)
  
  const fetchEventProfile = async () => {
  loading.value = true
  try {
    const data = await eventStore.fetchEventDetail(route.params.eventId) // ✅ use cache
    event.value = data.event
    attendees.value = data.attendees
  } catch (error) {
    console.error('Failed to load event:', error)
    toast.error('Failed to load event.')
    event.value = null
  } finally {
    loading.value = false
  }
}
  
  const formatDate = (dateString) => {
    const options = { dateStyle: 'medium', timeStyle: 'short' }
    return new Date(dateString).toLocaleString(undefined, options)
  }
  
  onMounted(fetchEventProfile)
  </script>
  
  <style scoped>
  </style>
  