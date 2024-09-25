<script setup lang="ts">
import { ref } from 'vue'
import useDragAndDrop from '@/utils/useDragAndDrop'

const { onDragStart } = useDragAndDrop()
const displayDevices = ref(false)

const openDevices = () => {
  displayDevices.value = !displayDevices.value

  const menu = document.getElementById('devices_menu')
  menu!.ariaExpanded = displayDevices.value.toString()
}

import { devices } from '@/assets/mock_data'
</script>

<template>
  <div
    aria-expanded="false"
    id="devices_menu"
    @click="openDevices"
    class="absolute right-0 z-50 h-9 rounded-xl border border-accent-500 bg-primary-100 px-4 leading-8 shadow-md aria-expanded:pb-4"
  >
    <div class="flex hover:cursor-pointer">
      <h3>Stored Devices</h3>
      <svg
        v-if="!displayDevices"
        class="ml-1 mt-px"
        xmlns="http://www.w3.org/2000/svg"
        width="32"
        height="32"
        viewBox="0 -960 960 960"
      >
        <path d="M480-344 240-584l56-56 184 184 184-184 56 56z" />
      </svg>
      <svg
        v-if="displayDevices"
        class="ml-1 mt-px"
        xmlns="http://www.w3.org/2000/svg"
        width="32"
        height="32"
        viewBox="0 -960 960 960"
      >
        <path d="M480-528 296-344l-56-56 240-240 240 240-56 56z" />
      </svg>
    </div>
    <div
      v-if="displayDevices"
      class="absolute right-0 top-12 z-50 max-h-[calc(100vh-8rem)] w-[16rem] overflow-scroll rounded-xl border border-accent-500 bg-primary-200 p-2"
    >
      <ul class="flex flex-col gap-2">
        <li
          :key="device.id"
          :draggable="true"
          @dragstart="onDragStart($event, device)"
          v-for="device in devices"
          class="rounded-lg bg-primary-100 px-4 py-1.5 shadow-md hover:cursor-grab"
        >
          <h4>{{ device.data?.label }}</h4>
        </li>
      </ul>
    </div>
  </div>
</template>
