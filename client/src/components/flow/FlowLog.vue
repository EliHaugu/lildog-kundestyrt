<script setup lang="ts">
defineProps<{
  show: boolean
}>()

import ListView from '@/components/log/ListView.vue'
import { logItems } from '@/assets/mock_data'
import { ref } from 'vue'
import WebSocketProvider from '@/providers/WebSocketProvider.vue'

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
          class="h-fit w-fit flex-shrink-0 rounded-lg bg-primary-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400 dark:hover:bg-accent-600 dark:aria-expanded:bg-accent-500"
        >
          All Devices
        </li>
        <li
          :key="item.id"
          v-for="item in logItems"
          @click="currentDevice = item.id"
          :aria-expanded="currentDevice === item.id"
          tabindex="1"
          class="h-fit w-fit flex-shrink-0 rounded-lg bg-primary-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400 dark:hover:bg-accent-600 dark:aria-expanded:bg-accent-500"
        >
          {{ item.name }}
        </li>
      </ul>
    </nav>
    <WebSocketProvider>
      <log-list :device-id="currentDevice" />
    </WebSocketProvider>
  </div>
</template>
