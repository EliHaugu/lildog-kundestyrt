<script setup lang="ts">
// import { MiniMap } from '@vue-flow/minimap'
import { listItems } from '@/assets/mock_data'
import { Background } from '@vue-flow/background'
import { VueFlow } from '@vue-flow/core'
import type { Edge } from '@vue-flow/core'
import type { CustomNode } from '@/types'
import FlowLog from '@/components/FlowLog.vue'
import FlowNode from '@/components/FlowNode.vue'
import { ref } from 'vue'

const stripNodeStyles = {
  backgroundColor: 'transparent',
  border: 'none',
  padding: '0',
  width: 'fit-content'
}

const nodes = ref<CustomNode[]>([
  {
    id: '1',
    data: { label: 'Button Press', connection: 'BLE' },
    position: { x: 400, y: 50 },
    style: stripNodeStyles
  },
  {
    id: '2',
    data: { label: 'Backend Updated', connection: 'ADE' },
    position: { x: 150, y: 200 },
    style: stripNodeStyles
  },
  {
    id: '3',
    data: { label: 'Driver Signal', connection: 'BLE' },
    position: { x: 650, y: 200 },
    style: stripNodeStyles
  },
  {
    id: '4',
    data: { label: 'Light Turned On', connection: 'WiFi' },
    position: { x: 400, y: 350 },
    style: stripNodeStyles
  }
])

const edges = ref<Edge[]>([
  { id: 'e1-2', source: '1', target: '2', type: 'smoothstep' },
  { id: 'e1-3', source: '1', target: '3', type: 'smoothstep' },
  { id: 'e3-4', source: '3', target: '4', type: 'smoothstep' }
])

const displayLog = ref(false)
</script>

<template>
  <main class="flex flex-col">
    <header class="mr-4 flex gap-2">
      <h1>{{ listItems.find((item) => item.id === $route.params.id)?.name }}</h1>
      <button class="ml-auto h-9 rounded-lg bg-accent-600 px-4 text-white-100">Run</button>
      <h3 class="h-9 rounded-lg border border-accent-500 px-4 leading-9">Stored Devices</h3>
    </header>
    <flow-log :show="displayLog" />
    <section class="mt-2 h-[calc(100vh-10rem)] w-[calc(100vw-18rem)]">
      <VueFlow v-if="!displayLog" v-model:nodes="nodes" v-model:edges="edges">
        <!--  MiniMap element only available if auto sized elements are not used -->
        <!--  <MiniMap class="rounded-lg" pannable zoomable /> -->
        <template #node-default="customNodeProps">
          <FlowNode v-bind="customNodeProps" />
        </template>
        <Background />
      </VueFlow>
    </section>
    <button @click="displayLog = !displayLog" class="fixed bottom-6 right-4" tabindex="1">
      Display log: {{ displayLog }}
    </button>
  </main>
</template>
