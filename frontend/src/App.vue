<template>
  <div id="app" class="min-h-screen w-screen overflow-x-hidden max-w-none">
    <Navbar v-if="showNavbar" />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { useRoute } from 'vue-router'
import { computed, onMounted } from 'vue'

const updateColor = () => {
  const color = localStorage.getItem('userColor') || '#6366f1'
  document.documentElement.style.setProperty('--btn-primary', color)

  const hoverColor = darkenColor(color, 10)
  document.documentElement.style.setProperty('--btn-primary-hover', hoverColor)
}

function darkenColor(hex, percent) {
  const num = parseInt(hex.replace("#", ""), 16)
  const amt = Math.round(2.55 * percent)
  const R = (num >> 16) - amt
  const G = (num >> 8 & 0x00FF) - amt
  const B = (num & 0x0000FF) - amt
  return `#${(
    0x1000000 +
    (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
    (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
    (B < 255 ? (B < 1 ? 0 : B) : 255)
  )
    .toString(16)
    .slice(1)}`
}


const route = useRoute()
const hideNavbarOnRoutes = ['/', '/login', '/signup']
const showNavbar = computed(() => !hideNavbarOnRoutes.includes(route.path))

onMounted(() => {
  updateColor()
})

</script>



<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
  max-width: 100vw; /* <-- ADD THIS */
}
</style>