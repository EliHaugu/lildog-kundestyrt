<script setup lang="ts">
import type { Log } from '@/types/WebSocketServiceTypes'
import type { IWebSocketService } from '@/interfaces/IWebSocketService'
import { reactive, onMounted, onUnmounted, inject, watch } from 'vue'
import { logItems } from '@/assets/mock_data'

const props = defineProps<{
  deviceId: number
  devices: { key: number; item: number }[]
}>()

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

watch(
  () => props.devices.length,
  () => {
    const el = document.getElementById(`log-${props.devices[0].item}`)

    if (!el) return
    if (props.devices.length % 2 === 0) {
      el.style.gridRow = 'span 1'
      return
    }

    switch (props.devices.length) {
      case 3:
        el.style.gridRow = 'span 2'
        break
      case 4:
        el.style.gridRow = 'span 3'
        break
      default:
        el.style.gridRow = 'span 4'
    }
  }
)
</script>

<template>
  <section
    :id="`log-${deviceId}`"
    class="mb-8 h-full overflow-y-scroll rounded-md bg-white-100 shadow-md dark:bg-accent-800"
    :class="{
      'grid-rows-subgrid': devices.length > 2 && devices.length % 2 !== 0
    }"
  >
    <h2 class="text-md pl-4 pt-2">
      {{ logItems.find((item) => item.id === deviceId)?.name || 'All Devices' }}
    </h2>
    <ul v-if="deviceId !== 0">
      <li
        v-for="log in state.logs.filter((item) => item.id === deviceId)"
        :key="log.id"
        class="m-2"
      >
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
