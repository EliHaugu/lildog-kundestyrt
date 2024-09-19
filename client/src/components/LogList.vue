<script setup lang="ts">
defineProps<{
  deviceId: number
}>()

import { defineProps, reactive, onMounted, onUnmounted } from 'vue';
import { webSocketService } from '@/services/WebSocketService';

const state = reactive({
  logs: [] as { id: number, log: string }[]
});

const handleNewLog = (log: { id: number, log: string }) => {
  state.logs.push(log);
};

onMounted(() => {
  webSocketService.connect(8765); // TODO: Should be called when test is run (but there is no such function yet)
  webSocketService.subscribe(handleNewLog); 
});


onUnmounted(() => {
  webSocketService.unsubscribe(handleNewLog);
});

</script>
<template>
  <section class="mb-8 h-full max-h-[calc(100vh-14rem)] overflow-y-scroll">
    <ul v-if="deviceId !== 0">
      <li v-for="log in state.logs.filter((item) => item.id === deviceId)?.log" :key="log.log">
        {{ log.log }}
      </li>
    </ul>
    <ul v-else>
      <li
        :key="deviceLogItem.log"
        v-for="deviceLogItem in state.logs"
      >
        {{ deviceLogItem.log }}
      </li>
    </ul>
  </section>
</template>
