<template>
  <div class="landing-container">

  </div>
</template>

<script setup>

</script>

<style scoped>
/* Layout background (gradient) */
.landing-container {
  @apply flex flex-col min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100;
}

/* Button styles */
.btn {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl text-lg transition-all duration-300;
}
</style>
