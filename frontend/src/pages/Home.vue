<template>
  <div class="landing-container">
    <!-- Left Side: Full Image -->
    <div class="w-1/2 h-full">
      <img src="@/assets/test1.webp" alt="City at sunset" class="w-full h-full object-cover" />
    </div>
    
    <!-- Right Side: Text + Buttons with background -->
    <div class="w-1/2 h-full bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex flex-col justify-center items-center p-16">
      <h1 class="text-6xl font-bold leading-tight mb-6 text-gray-800 text-center">
        go4friends
      </h1>
      <p class="text-2xl text-gray-600 mb-10 text-center">
        find friends on campus! 
      </p>
      <div class="flex space-x-6">
        <RouterLink to="/signup" class="btn">sign up</RouterLink>
        <RouterLink to="/login" class="btn">login</RouterLink>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  // No JS needed
  </script>
  
  <style>

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  html, body, #app {
    margin: 0;
    padding: 0;
    overflow: hidden;
    height: 100%;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
  }
  
  .landing-container {
    display: flex;
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    overflow: hidden;
  }
  
  </style>