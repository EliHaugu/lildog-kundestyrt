<script setup lang="ts">
defineProps<{
  show: boolean
}>()

import FlowLogList from './FlowLogList.vue'
import WebSocketProvider from '@/providers/WebSocketProvider.vue'

import { logItems } from '@/assets/mock_data'
import { ref } from 'vue'

const currentDevices = ref([{ key: 0, item: 0 }] as { key: number; item: number }[])

const modifyCurrentDevices = (id: number) => {
  const device = currentDevices.value.find((item) => item.item === id)
  if (device) {
    currentDevices.value = currentDevices.value.filter((item) => item.item !== id)
  } else {
    currentDevices.value.push({ key: Math.random(), item: id })
  }
}
</script>

<template>
  <div v-if="show">
    <nav class="mt-2 flex">
      <ul class="flex h-full flex-grow gap-2 overflow-x-scroll">
        <li
          @click="modifyCurrentDevices(0)"
          :aria-expanded="currentDevices.some((device) => device.item === 0)"
          tabindex="1"
          class="h-9 w-fit flex-shrink-0 rounded-md bg-primary-100 px-4 py-1.5 text-sm leading-6 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400 dark:hover:bg-accent-600 dark:aria-expanded:bg-accent-500"
        >
          All Devices
        </li>
        <li
          :key="item.id"
          v-for="item in logItems"
          @click="modifyCurrentDevices(item.id)"
          :aria-expanded="currentDevices.some((device) => device.item === item.id)"
          tabindex="1"
          class="h-9 w-fit flex-shrink-0 rounded-md bg-primary-100 px-4 py-1.5 text-sm leading-6 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500 aria-expanded:bg-accent-400 dark:hover:bg-accent-600 dark:aria-expanded:bg-accent-500"
        >
          {{ item.name }}
        </li>
      </ul>
    </nav>
    <div
      class="mr-4 grid h-[calc(100vh-10.75rem)] grid-cols-2 gap-2"
      :class="{ 'grid-cols-1': currentDevices.length === 1 }"
    >
      <web-socket-provider>
        <flow-log-list
          v-for="currentDevice in currentDevices"
          :key="currentDevice.item"
          :device-id="currentDevice.item"
          :devices="currentDevices"
        />
      </web-socket-provider>
    </div>
  </div>
</template>
