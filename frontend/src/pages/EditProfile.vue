<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <main class="flex-1 flex items-center justify-center pt-24 px-4">
      <div class="bg-white/20 backdrop-blur-md rounded-2xl p-8 w-full max-w-lg shadow-lg">
        <h1 class="text-3xl font-extrabold text-center text-gray-800 mb-8">Edit Profile</h1>

        <form @submit.prevent="updateProfile" class="space-y-6">
          <!-- Full Name -->
          <div class="flex flex-col space-y-2">
            <label class="text-sm font-medium text-gray-700">Full Name</label>
            <input v-model="full_name" type="text" class="input" placeholder="Enter your full name" />
          </div>

          <!-- Bio -->
          <div class="flex flex-col space-y-2">
            <label class="text-sm font-medium text-gray-700">Bio</label>
            <textarea v-model="bio" rows="3" class="input" placeholder="Tell us about yourself..."></textarea>
          </div>

          <!-- Location -->
          <div class="flex flex-col space-y-2">
            <label class="text-sm font-medium text-gray-700">Location</label>
            <input v-model="location" type="text" class="input" placeholder="Where are you?" />
          </div>

          <!-- Profile Picture -->
          <div class="flex flex-col space-y-2">
            <label class="text-sm font-medium text-gray-700">Profile Picture</label>
            <input type="file" @change="handleFileChange" class="input" />
          </div>

          <!-- Interests -->
          <div class="flex flex-col space-y-2">
            <label class="text-sm font-medium text-gray-700">Interests</label>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(interest, idx) in interests"
                :key="idx"
                class="bg-purple-200 text-purple-800 text-sm font-semibold px-3 py-1 rounded-full flex items-center"
              >
                {{ interest }}
                <button type="button" class="ml-2 text-red-500" @click="removeInterest(idx)">✕</button>
              </span>
            </div>
            <input
              v-model="newInterest"
              type="text"
              class="input mt-2"
              placeholder="Add a new interest and press Enter"
              @keydown.enter.prevent="addInterest"
            />
          </div>
          <!-- Major -->
          <div class="space-y-2">
            <label for="major" class="block text-sm font-medium text-gray-700">Major</label>
            <input id="major" type="text" v-model="major" class="input" placeholder="Enter your major" />
          </div>

          <!--Grad Year-->
          <div class="space-y-2">
            <label for="graduation_year" class="block text-sm font-medium text-gray-700">Graduation Year</label>
            <input id="graduation_year" type="number" v-model="graduationYear" class="input" placeholder="2025" />
          </div>

          <!-- Save/Cancel -->
          <div class="flex justify-between items-center mt-8">
            <button type="button" @click="cancel" class="btn bg-gray-400 hover:bg-gray-500">Cancel</button>
            <button type="submit" class="btn">Save Changes</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useUserStore } from '@/stores/user'
import { authAxios } from '@/utils/axios'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const full_name = ref('')
const bio = ref('')
const location = ref('')
const interests = ref([])
const newInterest = ref('')
const profile_picture = ref(null)
const major = ref('')
const graduationYear = ref('')

const syncFieldsFromStore = () => {
  const user = userStore.currentUser
  if (user) {
    full_name.value = user.full_name || ''
    bio.value = user.bio || ''
    location.value = user.location || ''
    interests.value = user.interests || []
    major.value = user.major || ''
    graduationYear.value = user.graduation_year || ''
  }
}

onMounted(async () => {
  await userStore.fetchCurrentUser()
  syncFieldsFromStore()
})

const updateProfile = async () => {
  try {
    let payload
    let headers

    if (profile_picture.value) {
      payload = new FormData()
      payload.append('full_name', full_name.value)
      payload.append('bio', bio.value)
      payload.append('location', location.value)
      payload.append('profile_picture', profile_picture.value)
      payload.append('interests', JSON.stringify(interests.value))
      payload.append('major', major.value)
      if (graduationYear.value) {
        payload.append('graduation_year', graduationYear.value)
      }
      headers = { 'Content-Type': 'multipart/form-data' }
    } else {
      payload = {
        full_name: full_name.value,
        bio: bio.value,
        location: location.value,
        interests: interests.value,
        major: major.value,
      }
      if (graduationYear.value) {
        payload.graduation_year = graduationYear.value
      }
      headers = { 'Content-Type': 'application/json' }
    }

    await authAxios.patch('/users/me/update/', payload, { headers })

    // ✅ Instantly update the store instead of refetching
    userStore.currentUser = {
      ...userStore.currentUser,
      full_name: full_name.value,
      bio: bio.value,
      location: location.value,
      interests: interests.value,
      major: major.value,
      graduation_year: graduationYear.value || null,
    }

    toast.success('Profile updated successfully!')
    router.push(`/profile/${userStore.currentUser.username}`)
  } catch (error) {
    console.error('Failed to update profile:', error)
    toast.error('Failed to update profile.')
  }
}


const handleFileChange = (e) => {
  profile_picture.value = e.target.files[0]
}

const addInterest = () => {
  const trimmed = newInterest.value.trim()
  if (trimmed && !interests.value.includes(trimmed)) {
    interests.value.push(trimmed)
    newInterest.value = ''
  }
}

const removeInterest = (idx) => {
  interests.value.splice(idx, 1)
}

const cancel = () => {
  router.push('/settings')
}
</script>
