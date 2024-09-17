<script setup lang="ts">
import { listItems } from '@/assets/mock_data'
import FlowLog from '@/components/FlowLog.vue'
import { ref } from 'vue'

const displayLog = ref(false)
</script>

<template>
  <main class="flex flex-col">
    <h1>{{ listItems.find((item) => item.id === $route.params.id)?.name }}</h1>

    <flow-log :show="displayLog" />
    <button @click="displayLog = !displayLog" class="fixed bottom-6 right-4" tabindex="1">
      Display log: {{ displayLog }}
    </button>
  </main>
</template>
