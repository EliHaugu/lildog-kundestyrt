<script setup lang="ts">
import NavButton from './PageNavigationButton.vue'
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
  <div class="flex h-screen min-w-max flex-col gap-12 bg-accent-800 py-5 pl-5">
    <h1 class="text-3xl font-light text-accent-400">liltest</h1>
    <nav class="flex flex-col gap-4">
      <nav-button to="/categories">
        <devices-icon class="w-12" />
        Configure Devices
      </nav-button>
      <nav-button to="/flow">
        <flows-icon class="w-12" />
        View flows
      </nav-button>
    </nav>
    <button @click="handleTheme" class="mt-auto" aria-label="Toggle colour mode">
      <theme-icon />
    </button>
  </div>
</template>
