<script setup lang="ts">
defineProps<{
  show: boolean
}>()
import { logItems } from '@/assets/mock_data'

</script>

<template >
  <section v-if="show" class="mt-4 w-ful flex gap-2">
    <ul class="flex h-14 flex-grow gap-2 overflow-x-scroll">
      <li
        class="h-fit w-fit flex-shrink-0 rounded-md bg-white-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500"
      >
        All Devices
      </li>
      <li
        key="item"
        v-for="item in logItems"
        class="h-fit w-fit flex-shrink-0 rounded-md bg-white-100 px-4 py-1.5 shadow-md transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500"
      >
        {{ item }}
      </li>
    </ul>
    <a
      href=""
      class="ml-auto mr-4 h-fit flex-shrink-0 rounded-md bg-accent-400 px-4 py-1.5 shadow-md transition-colors duration-200 hover:bg-accent-500"
      >Export log</a
    >
  </section>
</template>
