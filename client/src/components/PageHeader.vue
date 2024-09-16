<script setup lang="ts">
import { headerItems } from '@/assets/mock_data'
</script>
<template>
  <header class="fixed top-0 flex h-12 w-screen gap-40 bg-accent-800">
    <h1 class="ml-8 w-min text-2xl text-accent-400">liltest</h1>
    <ul class="ml-2 mr-auto flex flex-row gap-4">
      <li v-for="item in headerItems" v-bind:key="item.id" class="flex justify-center">
        <router-link
          :to="{ name: item.link }"
          tabindex="1"
          :aria-expanded="item.link === $route.path.split('/')[1]"
          class="my-auto rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-white-100 hover:text-accent-900 hover:shadow-lg aria-expanded:bg-white-100 aria-expanded:text-accent-900"
          >{{ item.name }}</router-link
        >
      </li>
    </ul>
  </header>
</template>
