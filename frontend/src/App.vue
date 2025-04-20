<template>
  <div id="app" class="min-h-screen w-screen overflow-x-hidden max-w-none">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
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