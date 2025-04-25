<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex flex-col items-center pt-24 px-6">
      <div class="w-full max-w-6xl flex flex-col sm:flex-row sm:items-center justify-between mb-10 space-y-4 sm:space-y-0">
        <h1 class="text-4xl font-extrabold text-gray-800">Upcoming Events</h1>
        <div class="flex space-x-4">
          <select v-model="filterType" class="input">
            <option value="">All</option>
            <option value="club">Club Events</option>
            <option value="school">School Events</option>
            <option value="myClubs">My Club Events</option>
          </select>
          <select v-model="sortOrder" class="input">
            <option value="date">Sort by Date</option>
            <option value="title">Sort by Title</option>
          </select>
        </div>
      </div>

      <!-- Events Section: Only show one of these -->
      <div v-if="sortedEvents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl">
        <div
          v-for="event in sortedEvents"
          :key="event.id"
          @click="toggleExpand(event.id)"
          class="bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300 cursor-pointer relative"
        >
          <div class="absolute top-2 left-2">
            <span v-if="event.club" class="bg-primary text-white text-xs font-bold py-1 px-2 rounded-lg">
              {{ typeof event.club === 'object' ? event.club.name : event.club }}
            </span>
            <span v-else class="bg-green-500 text-white text-xs font-bold py-1 px-2 rounded-lg">
              School Event
            </span>
          </div>

          <!-- Delete Button (top right) -->
          <button
            v-if="isClubStaff(event.club)"
            @click.stop="requestDeleteEvent(event.id)"
            class="absolute top-2 right-2 text-red-600 hover:text-red-800 text-sm font-bold"
            title="Delete Event"
          >
            ✕
          </button>

          <p class="text-sm text-gray-600 mt-1">👥 {{ event.attendee_count }} going</p>

          <img
            v-if="event.image"
            :src="event.image"
            alt="Event Image"
            class="w-full h-40 object-cover rounded-xl mb-4"
          />

          <h3 class="text-2xl font-bold text-gray-800">{{ event.title }}</h3>

          <!-- ✅ Location -->
          <p class="text-sm text-indigo-600 font-medium mt-1">
            📍 {{ event.location || 'No location specified' }}
          </p>

          <!-- Date -->
          <p class="text-sm text-gray-500 mt-1">{{ formatDate(event.date) }}</p>

          <!-- Description (only if expanded) -->
          <p v-if="expandedEventId === event.id" class="text-gray-700 mt-4">
            {{ event.description }}
          </p>

          <div class="mt-4">
            <button
              v-if="event.is_going"
              @click.stop="cancelRsvp(event.id)"
              class="redbtn"
            >
              Cancel RSVP
            </button>
            <button
              v-else
              @click.stop="rsvp(event.id)"
              class="btn"
            >
              RSVP
            </button>
          </div>
        </div>
      </div>

      <!-- No Events Message -->
      <div v-else class="text-gray-500 text-lg mt-10">No events yet. Be the first to create one!</div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-md text-center space-y-4">
          <h2 class="text-xl font-bold text-red-600">Delete Event</h2>
          <p class="text-gray-600">Are you sure you want to permanently delete this event?</p>
          <div class="flex justify-center space-x-4">
            <button class="btn" @click="showDeleteConfirm = false">Cancel</button>
            <button class="redbtn" @click="confirmDeleteEvent">Delete</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useEventStore } from '@/stores/events'
import { useClubStore } from '@/stores/club'

const eventStore = useEventStore()
const clubStore = useClubStore()
const toast = useToast()

const eventType = ref('school')
const clubName = ref('')
const newTitle = ref('')
const newDescription = ref('')
const newDate = ref('')
const newImage = ref(null)
const expandedEventId = ref(null)

const filterType = ref('')
const sortOrder = ref('date')

const showDeleteConfirm = ref(false)
const eventToDelete = ref(null)

const handleFileChange = (e) => {
  newImage.value = e.target.files[0]
}

const toggleExpand = (eventId) => {
  expandedEventId.value = expandedEventId.value === eventId ? null : eventId
}

const formatDate = (dateString) => {
  const options = { dateStyle: 'medium', timeStyle: 'short' }
  return new Date(dateString).toLocaleString(undefined, options)
}

const filteredEvents = computed(() => {
  if (!filterType.value) return eventStore.events

  if (filterType.value === 'club') {
    return eventStore.events.filter(event => event.club)
  }

  if (filterType.value === 'school') {
    return eventStore.events.filter(event => !event.club)
  }

  if (filterType.value === 'myClubs') {
    const myClubNames = clubStore.myClubs.map(club => club.name)
    return eventStore.events.filter(
      event => event.club && myClubNames.includes(event.club)
    )
  }

  return eventStore.events
})

const sortedEvents = computed(() => {
  return [...filteredEvents.value].sort((a, b) => {
    if (sortOrder.value === 'date') return new Date(a.date) - new Date(b.date)
    return a.title.localeCompare(b.title)
  })
})

const rsvp = async (eventId) => {
  try {
    await eventStore.rsvp(eventId)
    toast.success("You’re going!")
  } catch {
    toast.error("Could not RSVP")
  }
}

const cancelRsvp = async (eventId) => {
  try {
    await eventStore.cancelRsvp(eventId)
    toast.success("RSVP cancelled.")
  } catch {
    toast.error("Could not cancel RSVP")
  }
}

const isClubStaff = (clubName) => {
  const myClub = clubStore.myClubs.find(c => c.name === clubName)
  return myClub && ['admin', 'moderator'].includes(myClub.role)
}

const requestDeleteEvent = (eventId) => {
  eventToDelete.value = eventId
  showDeleteConfirm.value = true
}

const confirmDeleteEvent = async () => {
  if (!eventToDelete.value) return
  try {
    await eventStore.deleteEvent(eventToDelete.value)
    toast.success("Event deleted.")
    await eventStore.fetchEvents()
  } catch (err) {
    console.error(err)
    toast.error("Failed to delete event.")
  } finally {
    showDeleteConfirm.value = false
    eventToDelete.value = null
  }
}

onMounted(async () => {
  await clubStore.fetchClubs()
  await clubStore.fetchMyClubs()
  await eventStore.fetchEvents()
})
</script>


<style scoped>

</style>

  
  