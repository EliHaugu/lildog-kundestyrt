<script setup lang="ts">
import { listItems } from '@/assets/mock_data'
import BaseButton from '@/components/common/BaseButton.vue'
import ExitIcon from '@/icons/ExitIcon.vue'
import NodesList from '@/components/flow/NodesList.vue'
import ExportIcon from '@/icons/ExportIcon.vue'

defineEmits(['update:displayLog'])
defineProps({
  displayLog: Boolean,
  nodes: Array
})
</script>

<template>
  <header
    class="relative flex items-center gap-2 rounded-xl bg-white-100 p-2 shadow-md dark:bg-accent-800"
  >
    <router-link to="/flow" aria-label="Return to all flows" class="group"
      ><exit-icon
    /></router-link>
    <h1>
      {{ listItems.find((item) => item.id === $route.params.id)?.name }}
    </h1>

    <div class="ml-auto flex gap-2">
      <base-button
        @click="$emit('toggle-web-socket')"
        :variant="isRunning ? 'red' : 'default'"
        class="h-9 rounded-lg leading-tight"
      >
        {{ isRunning ? 'Stop' : 'Run' }}
      </base-button>
      <base-button
        :aria-expanded="displayLog"
        @click="$emit('toggle-log')"
        class="h-9 rounded-lg leading-tight aria-expanded:bg-accent-500"
      >
        Logs
      </base-button>

      <nodes-list v-if="!displayLog" :nodes="nodes" />
      <base-button
        v-else
        variant="light"
        class="inline-flex h-9 w-48 justify-center gap-2 rounded-lg leading-tight"
      >
        Export log
        <export-icon />
      </base-button>
    </div>
  </header>
</template>
