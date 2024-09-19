<script setup lang="ts">
import type { CustomData } from '@/types'
import { Handle, Position, NodeProps } from '@vue-flow/core'

defineProps<NodeProps<CustomData>>()
</script>
<template>
  <div class="rounded-xl border border-accent-500 bg-white-200 p-4 aria-expanded:h-64">
    <h1 class="text-lg">
      {{ data.label }}
    </h1>
    <div class="rounded-md bg-accent-400 px-4 py-2">
      <p>Connected through {{ data.connection }}</p>
    </div>
    <Handle type="target" :position="Position.Top" />
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>
