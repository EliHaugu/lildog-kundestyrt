<script setup lang="ts">
defineProps<{
  deviceId: number
}>()

import { reactive, onMounted, onUnmounted, inject } from 'vue'
import type { Log } from '@/types/WebSocketServiceTypes'
import type { IWebSocketService } from '@/interfaces/IWebSocketService'

const webSocketService = inject<IWebSocketService>('webSocketService')

const state = reactive({
  logs: [] as Log[]
})

const handleNewLog = (log: Log) => {
  state.logs.push(log)
}

onMounted(() => {
  if (webSocketService) {
    webSocketService.connect(8765)
    webSocketService.subscribe(handleNewLog)
  } else {
    console.error('WebSocketService not found')
  }
})

onUnmounted(() => {
  if (webSocketService) {
    webSocketService.unsubscribe(handleNewLog)
  }
})
</script>
<template>
  <section class="mb-8 h-full max-h-[calc(100vh-14rem)] overflow-y-scroll">
    <ul v-if="deviceId !== 0">
      <li v-for="log in state.logs.filter((item) => item.id === deviceId)" :key="log.id">
        {{ log.log }}
      </li>
    </ul>
    <ul v-else>
      <li :key="deviceLogItem.id" v-for="deviceLogItem in state.logs">
        {{ deviceLogItem.log }}
      </li>
    </ul>
  </section>
</template>
