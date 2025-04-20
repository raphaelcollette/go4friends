<template>
  <nav class="w-full p-4 flex justify-between items-center bg-white/30 backdrop-blur-md shadow-md fixed top-0 z-50">
    <RouterLink to="/" class="text-2xl font-bold text-purple-700">
      whatsurmajor
    </RouterLink>

    <div class="flex space-x-4">
      <RouterLink to="/main" class="btn">Feed</RouterLink>   <!-- NEW BUTTON -->
      <RouterLink to="/profile" class="btn">Profile</RouterLink>
    </div>
  </nav>
</template>

<script setup>
// no script needed
</script>

<style scoped>
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-xl text-base transition-all duration-300;
}
</style>