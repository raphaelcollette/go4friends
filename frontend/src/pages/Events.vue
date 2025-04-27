<template>
  <div class="flex flex-col min-h-screen w-screen overflow-x-hidden" style="background-image: var(--page-background); background-size: cover; background-position: center;">
    <main class="flex-1 flex flex-col items-center pt-24 px-6 relative">

      <!-- Main Layout -->
      <div class="flex w-full max-w-7xl space-x-6">
        
        <!-- Main Content (Events) -->
        <div class="flex-1">
          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-10 space-y-4 sm:space-y-0">
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

          <!-- Events Grid -->
          <div v-if="sortedEvents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-8">
            <div
              v-for="event in sortedEvents"
              :key="event.id"
              class="glossy-bg rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300 relative"
            >
              <!-- Edit/Delete Buttons -->
              <button v-if="isClubStaff(event.club)" @click.stop="requestDeleteEvent(event.id)" class="absolute top-2 right-2 text-red-600 hover:text-red-800 text-sm font-bold">✕</button>
              <button v-if="isClubStaff(event.club)" @click.stop="openEditModal(event)" class="absolute top-2 right-8 text-blue-600 hover:text-blue-800 text-sm font-bold">✏️</button>

              <RouterLink :to="`/events/${event.id}`" class="flex flex-col items-center text-center w-full">
                <div class="absolute top-2 left-2">
                  <span v-if="event.club" class="bg-primary text-white text-xs font-bold py-1 px-2 rounded-lg">
                    {{ typeof event.club === 'object' ? event.club.name : event.club }}
                  </span>
                  <span v-else class="bg-green-500 text-white text-xs font-bold py-1 px-2 rounded-lg">
                    School Event
                  </span>
                </div>

                <img v-if="event.image" :src="event.image" alt="Event Image" class="w-full h-40 object-cover rounded-xl mb-4" />
                <h3 class="text-2xl font-bold text-gray-800">{{ event.title }}</h3>
                <p class="text-sm text-indigo-600 font-medium mt-1">
                  📍 {{ event.location || 'No location specified' }}
                </p>
                <p class="text-sm text-gray-500 mt-1">{{ formatDate(event.date) }}</p>
              </RouterLink>

              <!-- RSVP Buttons outside the RouterLink -->
              <div class="mt-4">
                <button v-if="event.is_going" @click.stop="cancelRsvp(event.id)" class="redbtn">Cancel RSVP</button>
                <button v-else @click.stop="rsvp(event.id)" class="btn">RSVP</button>
              </div>
            </div>
          </div>

          <!-- No Events Message -->
          <div v-else class="text-gray-500 text-lg mt-10">
            No events yet. Be the first to create one!
          </div>
        </div>

        <!-- Suggested Events Sidebar -->
        <div class="w-72 hidden lg:block">
          <div class="glossy-bg p-6 rounded-2xl shadow-md space-y-4 sticky top-32">
            <h2 class="text-xl font-bold text-gray-800 mb-4">🔥 Suggested Events</h2>

            <div v-if="suggestedEvents.length > 0" class="space-y-3">
              <div
                v-for="event in suggestedEvents"
                :key="event.id"
                class="bg-white/30 backdrop-blur rounded-lg p-3 hover:brightness-110 transition cursor-pointer"
                @click="goToEvent(event.id)"
              >
                <p class="font-semibold text-gray-700">{{ event.title }}</p>
                <p class="text-xs text-gray-500">
                  {{ event.match_reasons ? event.match_reasons.join(' | ') : 'Suggested for you' }}
                </p>
              </div>
            </div>

            <div v-else class="text-gray-500 text-sm">
              No event suggestions at the moment.
            </div>
          </div>
        </div>

      </div>

      <!-- Delete Event Modal -->
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

      <!-- Edit Event Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-2xl shadow-lg w-full max-w-lg space-y-4">
          <h2 class="text-xl font-bold text-blue-600">Edit Event</h2>

          <input v-model="editForm.title" class="input w-full" placeholder="Title" />
          <input v-model="editForm.date" type="datetime-local" class="input w-full" />
          <input v-model="editForm.location" class="input w-full" placeholder="Location" />
          <textarea v-model="editForm.description" class="input w-full" placeholder="Description" rows="4" />
          <input type="file" @change="e => editForm.image = e.target.files[0]" class="input w-full" />

          <div class="flex justify-end space-x-4">
            <button class="btn" @click="showEditModal = false">Cancel</button>
            <button class="btn" @click="submitEditEvent">Save Changes</button>
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
import { useRouter } from 'vue-router'

const router = useRouter()
const eventStore = useEventStore()
const clubStore = useClubStore()
const toast = useToast()

const suggestedEvents = computed(() => eventStore.suggestedEvents)
const expandedEventId = ref(null)
const showEditModal = ref(false)
const eventToEdit = ref(null)

const filterType = ref('')
const sortOrder = ref('date')

const showDeleteConfirm = ref(false)
const eventToDelete = ref(null)

const editForm = ref({
  title: '',
  description: '',
  date: '',
  location: '',
  image: null
})

const submitEditEvent = async () => {
  if (!eventToEdit.value) return

  try {
    const formData = new FormData()
    formData.append('title', editForm.value.title)
    formData.append('description', editForm.value.description)
    formData.append('date', editForm.value.date)
    formData.append('location', editForm.value.location)

    if (editForm.value.image) {
      formData.append('image', editForm.value.image)
    }

    await eventStore.updateEvent(eventToEdit.value.id, formData)
    toast.success("Event updated!")
    await eventStore.fetchEvents(true)
    await eventStore.fetchSuggestedEvents(true)
    showEditModal.value = false
    eventToEdit.value = null
  } catch (err) {
    console.error(err)
    toast.error("Failed to update event")
  }
}

const openEditModal = (event) => {
  eventToEdit.value = event
  showEditModal.value = true
  editForm.value = {
    title: event.title,
    description: event.description,
    date: event.date,
    location: event.location || '',
    image: null
  }
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
    await eventStore.fetchEvents(true)
    await eventStore.fetchSuggestedEvents(true)
  } catch {
    toast.error("Could not RSVP")
  }
}

const cancelRsvp = async (eventId) => {
  try {
    await eventStore.cancelRsvp(eventId)
    toast.success("RSVP cancelled.")
    await eventStore.fetchEvents(true)
    await eventStore.fetchSuggestedEvents(true)
  } catch {
    toast.error("Could not cancel RSVP")
  }
}

const isClubStaff = (club) => {
  const clubName = typeof club === 'object' ? club.name : club
  return clubStore.myClubs.some(c => c.name === clubName && ['admin', 'moderator'].includes(c.role))
}

const goToEvent = (eventId) => {
  router.push(`/events/${eventId}`)
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
    await eventStore.fetchEvents(true)
    await eventStore.fetchSuggestedEvents(true)
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
  await eventStore.fetchSuggestedEvents()
})
</script>



<style scoped>

</style>

  
  