<template>
  <slot />
</template>

<script setup lang="ts">
import { provide } from 'vue'
import { webSocketService } from '@/services/WebSocketService'
import type { IWebSocketService } from '@/interfaces/IWebSocketService'

provide<IWebSocketService>('webSocketService', webSocketService)
</script>
