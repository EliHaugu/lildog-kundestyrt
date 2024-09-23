<script setup lang="ts">
import type { CustomData } from '@/types/nodeType'
import { Handle, Position } from '@vue-flow/core'
import type { NodeProps } from '@vue-flow/core'

defineProps<NodeProps<CustomData>>()

const expandNode = (event: Event) => {
  const clickedElement = event.currentTarget as HTMLElement

  if (clickedElement.getAttribute('aria-expanded') === 'true') {
    clickedElement.setAttribute('aria-expanded', 'false')
    return
  }

  document.querySelectorAll('.flow_node').forEach((node) => {
    node.setAttribute('aria-expanded', 'false')
  })
  clickedElement.setAttribute('aria-expanded', 'true')
}
</script>
<template>
  <div
    aria-expanded="false"
    class="flow_node rounded-xl border border-accent-500 bg-white-200 p-4 aria-expanded:h-64"
    @click="expandNode($event)"
  >
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
