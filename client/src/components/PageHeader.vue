<script setup lang="ts">
import { headerItems } from '@/assets/mock_data'
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
  <header class="fixed top-0 flex h-12 w-screen gap-40 bg-accent-800">
    <h1 class="ml-8 w-min text-2xl text-accent-400">liltest</h1>
    <ul class="ml-2 mr-auto flex w-full flex-row gap-4">
      <li v-for="item in headerItems" :key="item.id" class="flex justify-center">
        <router-link
          :to="{ name: item.link }"
          tabindex="1"
          :aria-expanded="item.link === $route.path.split('/')[1]"
          class="my-auto rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-primary-200 hover:text-accent-900 hover:shadow-lg aria-expanded:bg-primary-200 aria-expanded:text-accent-900 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
          >{{ item.name }}</router-link
        >
      </li>
      <li class="ml-auto mr-4 mt-2 flex">
        <!-- <input type="checkbox" name="" id="darkMode" class="ml-auto" @change="handleTheme" /> -->
        <button @click="handleTheme" class="ml-auto">
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
      </li>
    </ul>
  </header>
</template>
