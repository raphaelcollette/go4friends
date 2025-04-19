<template>
    <div class="landing-container">
      <!-- Left Side: Full Image -->
      <div class="w-1/2 h-full">
        <img src="@/assets/test1.png" alt="City at sunset" class="w-full h-full object-cover" />
      </div>
      
      <!-- Right Side: Text + Buttons with background -->
      <div class="w-1/2 h-full bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex flex-col justify-center items-start p-16">
        <h1 class="text-6xl font-bold leading-tight mb-6 text-gray-800">
        <br />
          whatsurmajor?
        </h1>
        <p class="text-2xl text-gray-600 mb-10">
          find friends on campus! 
        </p>
        <div class="flex space-x-6">
          <RouterLink to="/signup" class="btn">Sign Up</RouterLink>
          <RouterLink to="/login" class="btn">Login</RouterLink>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  // No JS needed
  </script>
  
  <style>
  /* Reset styles to eliminate gaps and scrollbars */
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
  
  .btn {
    @apply bg-purple-600 text-white py-3 px-8 rounded-lg text-lg hover:bg-purple-700 transition-all duration-300;
  }
  </style>