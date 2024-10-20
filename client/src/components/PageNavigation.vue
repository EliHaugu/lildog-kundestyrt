<script setup lang="ts">
import DevicesIcon from '@/icons/DevicesIcon.vue'
import FlowsIcon from '@/icons/FlowsIcon.vue'
import ThemeIcon from '@/icons/ThemeIcon.vue'
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
    <h1 class="ml-4 w-min text-3xl font-light text-accent-400">liltest</h1>
    <nav class="mt-16 flex flex-col gap-2">
      <router-link
        to="/devices"
        :aria-expanded="$route.path.includes('/devices')"
        class="text-md nav_item__rounded relative z-10 inline-flex items-center gap-2 rounded-l-xl fill-white-100 py-1.5 pl-4 pr-2 leading-10 text-white-100 hover:z-50 hover:cursor-pointer hover:bg-primary-300 hover:fill-accent-500 hover:text-accent-900 hover:shadow-xl hover:transition-colors hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:fill-accent-500 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
        ><devices-icon /> Configure Devices</router-link
      >
      <router-link
        to="/flows"
        :aria-expanded="$route.path.includes('/flows')"
        class="text-md nav_item__rounded relative z-10 inline-flex items-center gap-2 rounded-l-xl fill-white-100 py-1.5 pl-4 pr-2 leading-10 text-white-100 hover:z-50 hover:cursor-pointer hover:bg-primary-300 hover:fill-accent-500 hover:text-accent-900 hover:shadow-xl hover:transition-colors hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:fill-accent-500 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
        ><flows-icon /> View Flows</router-link
      >
    </nav>
    <button @click="handleTheme" class="absolute bottom-4">
      <theme-icon />
    </button>
  </section>
</template>
