<script setup lang="ts">
defineProps<{
  show: boolean
}>()

import LogList from '@/components/LogList.vue'
import { logItems } from '@/assets/mock_data'
import { ref } from 'vue'

const currentDevice = ref(0)
</script>

<template>
  <div v-if="show">
    <nav class="mt-2 flex gap-2">
      <ul class="flex h-14 flex-grow gap-2 overflow-x-scroll">
        <li
          @click="currentDevice = 0"
          :aria-expanded="currentDevice === 0"
          tabindex="1"
          class="h-fit w-fit flex-shrink-0 rounded-md bg-white-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400"
        >
          All Devices
        </li>
        <li
          :key="item.id"
          v-for="item in logItems"
          @click="currentDevice = item.id"
          :aria-expanded="currentDevice === item.id"
          tabindex="1"
          class="h-fit w-fit flex-shrink-0 rounded-md bg-white-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400"
        >
          {{ item.name }}
        </li>
      </ul>
      <a
        href=""
        tabindex="1"
        class="ml-auto mr-4 flex h-fit flex-shrink-0 gap-2 rounded-md bg-accent-400 px-4 py-1.5 shadow-md transition-colors duration-200 hover:bg-accent-500"
        >Export log
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          class="fill-accent-800"
          height="24"
          viewBox="0 -960 960 960"
        >
          <path
            d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58zM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160z"
          /></svg
      ></a>
    </nav>
    <log-list :device-id="currentDevice" />
  </div>
</template>
