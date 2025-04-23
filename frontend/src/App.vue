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
import { computed } from 'vue'

const route = useRoute()
const hideNavbarOnRoutes = ['/', '/login', '/signup']
const showNavbar = computed(() => !hideNavbarOnRoutes.includes(route.path))

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