<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDarkMode = ref(false)

function handleTheme() {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.body.classList.add('dark')
    localStorage.setItem('darkMode', 'true')
  } else {
    document.body.classList.remove('dark')
    localStorage.setItem('darkMode', 'false')
  }
}

onMounted(() => {
  const savedDarkMode = localStorage.getItem('darkMode')
  if (savedDarkMode === 'true') {
    isDarkMode.value = true
    document.body.classList.add('dark')
  } else {
    isDarkMode.value = false
    document.body.classList.remove('dark')
  }
})
</script>

<template>
  <section class="fixed left-0 top-0 h-screen w-64 bg-accent-800 pl-4">
    <h1 class="w-min text-3xl font-light text-accent-400 ml-4">liltest</h1>
    <nav class="mt-16 flex flex-col gap-2">
      <router-link
        to="/devices"
        :aria-expanded="$route.name === 'devices'"
        class="text-md nav_item__rounded relative z-10 inline-flex items-center gap-2 rounded-l-xl fill-white-100 py-1.5 pl-4 pr-2 leading-10 text-white-100 hover:z-50 hover:cursor-pointer hover:bg-primary-300 hover:fill-accent-500 hover:text-accent-900 hover:shadow-xl hover:transition-colors hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:fill-accent-500 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
        ><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 -960 960 960">
          <path
            d="M80-160v-120h80v-440q0-33 23.5-56.5T240-800h600v80H240v440h240v120zm520 0q-17 0-28.5-11.5T560-200v-400q0-17 11.5-28.5T600-640h240q17 0 28.5 11.5T880-600v400q0 17-11.5 28.5T840-160zm40-120h160v-280H640zm0 0h160z"
          /></svg
        >Configure Devices</router-link
      >
      <router-link
        to="/flows"
        :aria-expanded="$route.name === 'flows'"
        class="text-md nav_item__rounded relative z-10 inline-flex items-center gap-2 rounded-l-xl fill-white-100 py-1.5 pl-4 pr-2 leading-10 text-white-100 hover:z-50 hover:cursor-pointer hover:bg-primary-300 hover:fill-accent-500 hover:text-accent-900 hover:shadow-xl hover:transition-colors hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:fill-accent-500 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
        ><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 -960 960 960">
          <path
            d="M160-480v240-480zm400 360q17 0 28.5-11.5T600-160t-11.5-28.5T560-200t-28.5 11.5T520-160t11.5 28.5T560-120m240-400q17 0 28.5-11.5T840-560t-11.5-28.5T800-600t-28.5 11.5T760-560t11.5 28.5T800-520m-560 0h200v-80H240zm0 160h200v-80H240zm-80 200q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720H160v480h200v80zM560-40q-50 0-85-35t-35-85q0-39 22.5-70t57.5-43v-127h240v-47q-35-12-57.5-43T680-560q0-50 35-85t85-35 85 35 35 85q0 39-22.5 70T840-447v127H600v47q35 12 57.5 43t22.5 70q0 50-35 85t-85 35"
          /></svg
        >View Flows</router-link
      >
    </nav>
    <button @click="handleTheme" class="absolute bottom-4">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        class="text-accent-500 dark:text-white-200"
        viewBox="0 -960 960 960"
      >
        <path
          d="M480-120q-150 0-255-105T120-480t105-255 255-105q14 0 27.5 1t26.5 3q-41 29-65.5 75.5T444-660q0 90 63 153t153 63q55 0 101-24.5t75-65.5q2 13 3 26.5t1 27.5q0 150-105 255T480-120m0-80q88 0 158-48.5T740-375q-20 5-40 8t-40 3q-123 0-209.5-86.5T364-660q0-20 3-40t8-40q-78 32-126.5 102T200-480q0 116 82 198t198 82m-10-270"
          fill="currentColor"
        />
      </svg>
    </button>
  </section>
</template>
