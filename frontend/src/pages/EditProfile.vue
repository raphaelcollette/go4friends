<template>
  <div class="flex flex-col min-h-screen w-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 overflow-x-hidden">
    <Navbar />

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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAxios } from '@/utils/axios'
import Navbar from '@/components/Navbar.vue'
import { useToast } from 'vue-toastification'

// Setup Refs
const router = useRouter()
const toast = useToast()

const full_name = ref('')
const bio = ref('')
const location = ref('')
const interests = ref([])
const newInterest = ref('')
const profile_picture = ref(null)
const currentUsername = ref('')

// Fetch the current user's profile
const fetchProfile = async () => {
  try {
    const res = await authAxios.get('users/me/')
    full_name.value = res.data.full_name || ''
    bio.value = res.data.bio || ''
    location.value = res.data.location || ''
    interests.value = res.data.interests || []
    currentUsername.value = res.data.username
  } catch (error) {
    console.error('Failed to fetch profile:', error)
    toast.error('Failed to load your profile.')
    router.push('/settings')
  }
}

// Update profile
const updateProfile = async () => {
  try {
    let payload;
    let headers;

    if (profile_picture.value) {
      // If there is a file, use FormData
      payload = new FormData();
      payload.append('full_name', full_name.value);
      payload.append('bio', bio.value);
      payload.append('location', location.value);
      payload.append('profile_picture', profile_picture.value);
      payload.append('interests', JSON.stringify(interests.value));

      headers = { 'Content-Type': 'multipart/form-data' };
    } else {
      // Otherwise send normal JSON
      payload = {
        full_name: full_name.value,
        bio: bio.value,
        location: location.value,
        interests: interests.value,  // ✅ send as array
      };

      headers = { 'Content-Type': 'application/json' };
    }

    await authAxios.patch('users/me/update/', payload, { headers });

    toast.success('Profile updated successfully!');
    router.push(`/profile/${currentUsername.value}`);
  } catch (error) {
    console.error('Failed to update profile:', error.response?.data || error.message);
    toast.error('Failed to update profile.');
  }
};

// Handle file change
const handleFileChange = (event) => {
  profile_picture.value = event.target.files[0]
}

// Cancel editing
const cancel = () => {
  router.push('/settings')
}

// Add an interest
const addInterest = () => {
  const trimmed = newInterest.value.trim()
  if (trimmed && !interests.value.includes(trimmed)) {
    interests.value.push(trimmed)
    newInterest.value = ''
  }
}

// Remove an interest
const removeInterest = (index) => {
  interests.value.splice(index, 1)
}

// On Mount
onMounted(fetchProfile)
</script>

<style scoped>
.input {
  @apply w-full bg-white border border-gray-300 rounded-xl p-4 text-lg focus:outline-none focus:ring-2 focus:ring-purple-400;
}

.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300;
}
</style>