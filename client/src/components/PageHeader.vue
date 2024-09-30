<script setup lang="ts">
import { headerItems } from '@/assets/mock_data'

const handleTheme = (event: Event) => {
  const checkbox = event.target as HTMLInputElement
  const body = document.querySelector('body') as HTMLBodyElement

  if (checkbox.checked) {
    body.classList.add('dark')
    return
  }

  body.classList.remove('dark')
}
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
      <li class="ml-auto mr-4 mt-2 flex text-white-100">
        <input type="checkbox" name="" id="darkMode" class="ml-auto" @change="handleTheme" />
      </li>
    </ul>
  </header>
</template>
