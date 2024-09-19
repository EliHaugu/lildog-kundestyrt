<script setup lang="ts">
defineProps<{
  deviceId: number
}>()

import { logItems } from '@/assets/mock_data'
import { listItems } from '@/assets/mock_data'
</script>
<template>
  <section class="mb-8 h-full max-h-[calc(100vh-14rem)] overflow-y-scroll">
    <ul v-if="deviceId !== 0">
      <li v-for="log in logItems.find((item) => item.id === deviceId)?.log" :key="log">
        {{ log }}
      </li>
    </ul>
    <ul v-else>
      <li
        :key="deviceLogItem"
        v-for="deviceLogItem in logItems.flatMap((device) => device.log).sort()"
      >
        {{ deviceLogItem }}
      </li>
    </ul>
  </section>
</template>
