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
          </select>
          <select v-model="sortOrder" class="input">
            <option value="date">Sort by Date</option>
            <option value="title">Sort by Title</option>
          </select>
          <button class="btn" @click="showCreate = true">+ Create Event</button>
        </div>
      </div>

      <!-- Create Event Modal -->
      <div v-if="showCreate" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white rounded-2xl p-8 w-full max-w-md space-y-4">
          <h2 class="text-2xl font-bold text-center">Create Event</h2>

          <select v-model="eventType" class="input w-full">
            <option value="school">School-wide Event</option>
            <option value="club">Club Event</option>
          </select>

          <div v-if="eventType === 'club'">
            <select v-model="clubName" class="input w-full">
              <option disabled value="">Select Club</option>
              <option v-for="club in clubs" :key="club.id" :value="club.name">
                {{ club.name }}
              </option>
            </select>
          </div>

          <input v-model="newTitle" type="text" placeholder="Event Title" class="input w-full" />
          <textarea v-model="newDescription" placeholder="Event Description" class="input w-full"></textarea>
          <input v-model="newDate" type="datetime-local" class="input w-full" />
          <input type="file" @change="handleFileChange" class="input w-full" />

          <div class="flex justify-end space-x-4 mt-4">
            <button class="btn bg-gray-400 hover:bg-gray-500" @click="showCreate = false">Cancel</button>
            <button class="btn bg-green-500 hover:bg-green-600" @click="createEvent">Create</button>
          </div>
        </div>
      </div>

      <!-- Events List -->
      <div v-if="filteredEvents.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-full max-w-6xl">
        <div
          v-for="event in sortedEvents"
          :key="event.id"
          @click="toggleExpand(event.id)"
          class="bg-white/20 backdrop-blur-md rounded-2xl shadow-md p-6 flex flex-col items-center text-center hover:shadow-xl transition-all duration-300 cursor-pointer relative"
        >
          <div class="absolute top-2 left-2">
            <span v-if="event.club" class="bg-purple-500 text-white text-xs font-bold py-1 px-2 rounded-lg">
              {{ event.club }}
            </span>
            <span v-else class="bg-green-500 text-white text-xs font-bold py-1 px-2 rounded-lg">
              School Event
            </span>
          </div>

          <p class="text-sm text-gray-600 mt-1">👥 {{ event.attendee_count }} going</p>

          <img
            v-if="event.image"
            :src="event.image"
            alt="Event Image"
            class="w-full h-40 object-cover rounded-xl mb-4"
          />

          <h3 class="text-2xl font-bold text-gray-800">{{ event.title }}</h3>
          <p class="text-sm text-gray-500 mt-2">{{ formatDate(event.date) }}</p>

          <p v-if="expandedEventId === event.id" class="text-gray-700 mt-4">{{ event.description }}</p>

          <div class="mt-4">
            <button
              v-if="event.is_going"
              @click.stop="cancelRsvp(event.id)"
              class="btn bg-red-500 hover:bg-red-600"
            >
              Cancel RSVP
            </button>
            <button
              v-else
              @click.stop="rsvp(event.id)"
              class="btn bg-green-500 hover:bg-green-600"
            >
              RSVP
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-gray-500 text-lg mt-10">No events yet. Be the first to create one!</div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

const events = ref([])
const clubs = ref([])
const toast = useToast()

const showCreate = ref(false)
const eventType = ref('school')
const clubName = ref('')
const newTitle = ref('')
const newDescription = ref('')
const newDate = ref('')
const newImage = ref(null)
const expandedEventId = ref(null)

const filterType = ref('')
const sortOrder = ref('date')

const fetchEvents = async () => {
  try {
    const res = await authAxios.get('/events/', { params: { upcoming: true } })
    events.value = res.data
  } catch (error) {
    console.error(error)
    toast.error('Failed to load events.')
  }
}

const fetchClubs = async () => {
  try {
    const res = await authAxios.get('/clubs/')
    clubs.value = res.data
  } catch (error) {
    console.error(error)
    toast.error('Failed to load clubs.')
  }
}

const createEvent = async () => {
  if (!newTitle.value || !newDate.value) {
    toast.error('Title and date are required.')
    return
  }

  const formData = new FormData()
  formData.append('title', newTitle.value)
  formData.append('description', newDescription.value)
  formData.append('date', newDate.value)
  if (newImage.value) {
    formData.append('image', newImage.value)
  }
  if (eventType.value === 'club' && clubName.value) {
    formData.append('club_name', clubName.value)
  }

  try {
    await authAxios.post('/events/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    toast.success('Event created!')
    showCreate.value = false
    newTitle.value = ''
    newDescription.value = ''
    newDate.value = ''
    newImage.value = null
    clubName.value = ''
    fetchEvents()
  } catch (error) {
    console.error(error)
    toast.error('Failed to create event.')
  }
}

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
  if (!filterType.value) return events.value
  return events.value.filter(event =>
    filterType.value === 'club' ? event.club : !event.club
  )
})

const sortedEvents = computed(() => {
  return [...filteredEvents.value].sort((a, b) => {
    if (sortOrder.value === 'date') return new Date(a.date) - new Date(b.date)
    return a.title.localeCompare(b.title)
  })
})

const rsvp = async (eventId) => {
  try {
    await authAxios.post(`/events/${eventId}/rsvp/`)
    toast.success('You’re going!')
    fetchEvents()
  } catch (e) {
    toast.error('Could not RSVP')
  }
}

const cancelRsvp = async (eventId) => {
  try {
    await authAxios.post(`/events/${eventId}/cancel-rsvp/`)
    toast.success('RSVP cancelled.')
    fetchEvents()
  } catch (e) {
    toast.error('Could not cancel RSVP')
  }
}

onMounted(() => {
  fetchEvents()
  fetchClubs()
})
</script>

<style scoped>
.input {
  @apply p-3 rounded-xl bg-white/50 backdrop-blur-sm placeholder-gray-500 text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-400;
}

.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300;
}
</style>

  
  