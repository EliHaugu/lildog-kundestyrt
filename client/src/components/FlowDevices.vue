<script setup lang="ts">
import { ref } from 'vue'
import useDragAndDrop from '@/utils/useDragAndDrop'

const { onDragStart } = useDragAndDrop()
const displayDevices = ref(true)

const openDevices = () => {
  displayDevices.value = !displayDevices.value

  const menu = document.getElementById('devices_menu')
  menu!.ariaExpanded = displayDevices.value.toString()
}

const devices = ['Device 1', 'Device 2', 'Device 3']
</script>

<template>
  <div
    aria-expanded="true"
    id="devices_menu"
    class="absolute right-0 z-50 h-9 rounded-xl border border-accent-600 bg-white-100 px-4 leading-8 aria-expanded:h-auto aria-expanded:pb-4"
  >
    <div class="flex hover:cursor-pointer" @click="openDevices">
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
    <div v-if="displayDevices" class="">
      <ul class="flex flex-col gap-2">
        <li
          :key="device"
          :draggable="true"
          @dragstart="onDragStart($event, device)"
          v-for="device in devices"
          class="rounded-lg bg-accent-400 px-4 py-1.5"
        >
          <h4>{{ device }}</h4>
        </li>
      </ul>
    </div>
  </div>
</template>
