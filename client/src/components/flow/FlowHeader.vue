<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import ExitIcon from '@/icons/ExitIcon.vue'
import FlowDevices from '@/components/flow/FlowDevices.vue'
import ExportIcon from '@/icons/ExportIcon.vue'

const props = defineProps({
  displayLog: Boolean,
  nodes: Array,
  flow: Object
})

defineEmits(['update:displayLog'])
</script>
<template>
  <header
    class="relative mr-4 flex items-center gap-2 rounded-xl bg-white-100 p-2 shadow-md dark:bg-accent-800"
  >
    <a href="/flow" aria-label="Return to all flows" class="group"><exit-icon /></a>
    <h1>
      {{ props.flow?.name }}
    </h1>

    <div class="ml-auto flex gap-2">
      <base-button variant="default" class="h-9 rounded-lg leading-tight"> Run </base-button>
      <base-button @click="$emit('update:displayLog')" class="h-9 rounded-lg leading-tight">
        Logs
      </base-button>

      <flow-devices v-if="!displayLog" :nodes="nodes" />
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
