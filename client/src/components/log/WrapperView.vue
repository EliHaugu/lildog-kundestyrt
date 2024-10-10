<script setup lang="ts">
defineProps<{
  show: boolean
}>()

import LogList from '@/components/log/ListView.vue'
import { logItems } from '@/assets/mock_data'
import { ref } from 'vue'
import WebSocketProvider from '@/providers/WebSocketProvider.vue'
import BaseButton from '../BaseButton.vue'

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
    <nav class="mt-2 flex gap-2">
      <ul class="mb-4 flex flex-grow gap-2 overflow-x-scroll">
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
      <BaseButton class="mr-4 flex h-9" size="sm">
        Export log
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          class="fill-accent-800"
          height="24"
          viewBox="0 -960 960 960"
        >
          <path
            d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58zM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160z"
          />
        </svg>
      </BaseButton>
    </nav>
    <div
      class="mr-4 grid h-[calc(100vh-14rem)] grid-cols-2 gap-2"
      :class="{ 'grid-cols-1': currentDevices.length === 1 }"
    >
      <WebSocketProvider>
        <log-list
          v-for="currentDevice in currentDevices"
          :key="currentDevice.item"
          :device-id="currentDevice.item"
          :devices="currentDevices"
        />
      </WebSocketProvider>
    </div>
  </div>
</template>
