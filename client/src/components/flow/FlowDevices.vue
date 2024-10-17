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
import ChevronIcon from '@/icons/ChevronIcon.vue'
</script>

<template>
  <div
    aria-expanded="false"
    id="devices_menu"
    @click="openDevices"
    class="right-0 z-50 h-9 w-48 justify-center rounded-lg border border-accent-500 bg-primary-100 px-4 leading-8 shadow-md aria-expanded:pb-4"
  >
    <div class="flex hover:cursor-pointer">
      <h3>Stored Devices</h3>
      <chevron-icon :class="{ 'rotate-180 transform': displayDevices }" />
    </div>
    <div
      v-if="displayDevices"
      class="absolute right-0 top-12 z-50 max-h-[calc(100vh-8rem)] w-[16rem] rounded-xl border border-accent-500 bg-primary-200"
    >
      <ul
        class="mr-2 mt-2 flex max-h-[calc(100vh-9rem)] flex-col gap-2 overflow-y-scroll px-2 pb-2"
      >
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
