<script setup lang="ts">
// import { MiniMap } from '@vue-flow/minimap'
import { listItems } from '@/assets/mock_data'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/utils/useDragAndDrop'
import type { Connection, Edge, GraphEdge } from '@vue-flow/core'
import type { CustomNode } from '@/types/nodeType'
import FlowLog from '@/components/FlowLog.vue'
import FlowNode from '@/components/FlowNode.vue'
import FlowEdge from '@/components/FlowEdge.vue'
import FlowDevices from '@/components/FlowDevices.vue'
import { ref } from 'vue'
import { stripNodeStyles } from '@/utils/stripNodeStyles'
import BaseButton from '../components/BaseButton.vue'

const { onConnect, addEdges, updateEdge } = useVueFlow()
const { onDragOver, onDrop, onDragLeave } = useDragAndDrop()

onConnect(addEdges)

function onEdgeChange({ edge, connection }: { edge: GraphEdge; connection: Connection }) {
  updateEdge(
    {
      ...edge,
      type: 'smoothstep'
    },
    connection
  )
}

const nodes = ref<CustomNode[]>([
  {
    id: '1',
    data: {
      label: 'Button Press',
      connection: 'BLE',
      type: 'Action',
      testState: 'idle',
      fields: {
        uuid: '123456789',
        action: 'buttonPressed()'
      }
    },
    position: { x: 400, y: 50 },
    style: stripNodeStyles
  },
  {
    id: '2',
    data: {
      label: 'Backend Updated',
      connection: 'ADE',
      type: 'Action',
      testState: 'success',
      fields: {
        uuid: '987654321',
        action: 'updateBackend()'
      }
    },
    position: { x: 150, y: 200 },
    style: stripNodeStyles
  },
  {
    id: '3',
    data: {
      label: 'Driver Signal',
      connection: 'BLE',
      type: 'Assertion',
      testState: 'warning',
      fields: {
        uuid: '123456789',
        assertion: 'driverSignalSent()'
      }
    },
    position: { x: 650, y: 200 },
    style: stripNodeStyles
  },
  {
    id: '4',
    data: {
      label: 'Light Turned On',
      connection: 'WiFi',
      type: 'Assertion',
      testState: 'error',
      fields: {
        uuid: '987654321',
        assertion: 'lightIsOn()'
      }
    },
    position: { x: 400, y: 350 },
    style: stripNodeStyles
  }
])

const edges = ref<Edge[]>([
  { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', updatable: true },
  { id: 'e1-3', source: '1', target: '3', type: 'smoothstep', updatable: true },
  { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', updatable: true }
])

const displayLog = ref(false)
</script>

<template>
  <main class="flex flex-col">
    <header class="relative mr-4 flex h-10 gap-2">
      <h1>{{ listItems.find((item) => item.id === $route.params.id)?.name }}</h1>
      <BaseButton v-if="displayLog" variant="default" class="ml-auto h-9 pt-1 leading-tight">
        Run
      </BaseButton>
      <BaseButton v-else variant="default" class="ml-auto mr-48 h-9 pt-1 leading-tight">
        Run
      </BaseButton>
      <flow-devices v-if="!displayLog" :nodes="nodes" />
    </header>
    <flow-log :show="displayLog" />
    <section class="mt-2 h-[calc(100vh-10rem)] w-[calc(100vw-18rem)]" @drop="onDrop">
      <VueFlow
        v-if="!displayLog"
        v-model:nodes="nodes"
        v-model:edges="edges"
        @dragover="onDragOver"
        @dragleave="onDragLeave"
        @edge-update="onEdgeChange"
      >
        <!--  MiniMap element only available if auto sized elements are not used -->
        <!--  <MiniMap class="rounded-lg" pannable zoomable /> -->
        <template #node-default="customNodeProps">
          <flow-node v-bind="customNodeProps" />
        </template>
        <template #edge-default="edgeProps">
          <flow-edge v-bind="edgeProps" />
        </template>
        <Background />
      </VueFlow>
    </section>
    <button @click="displayLog = !displayLog" class="fixed bottom-6 right-4" tabindex="1">
      Display log: {{ displayLog }}
    </button>
  </main>
</template>
