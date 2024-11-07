<script setup lang="ts">
import FlowHeader from '@/components/flow/FlowHeader.vue'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/composables/useDragAndDrop'

import type { Connection, Edge, GraphEdge } from '@vue-flow/core'
import type { CustomNode } from '@/types/NodeType'
import type { Flows } from '@/types/FlowType'

import FlowLog from '@/components/flow/FlowLog.vue'
import FlowNode from '@/components/flow/FlowNode.vue'
import FlowEdge from '@/components/flow/FlowEdge.vue'

import { ref, type Ref } from 'vue'
import { inject, computed } from 'vue'
import { useRoute } from 'vue-router'
import { webSocketService } from '@/services/WebSocketService'
import type { Log } from '@/types/WebSocketServiceTypes'

const flows = inject<Ref<Flows>>('flows', ref([]))

const route = useRoute()
const flowId = route.params.id
const selectedFlow = computed(() => flows.value.find((flow) => flow.id === flowId))

const nodes = ref<CustomNode[]>(selectedFlow.value?.nodes || [])
const edges = ref<Edge[]>(selectedFlow.value?.edges || [])

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

const displayLog = ref(false)
const isRunning = ref(false)

const handleNewLog = (log: Log) => {
  console.log('new log', log)
}

// toggle log display
const isRunning = ref(false)

const handleNewLog = (log: Log) => {
  console.log('new log', log)
}

// toggle log display
const toggleLog = () => {
  displayLog.value = !displayLog.value
}

// toggle websocket connection
const toggleWebSocket = () => {
  isRunning.value = !isRunning.value

  if (isRunning.value) {
    webSocketService.connect(8765)
    webSocketService.subscribe(handleNewLog)
  } else {
    webSocketService.unsubscribe(handleNewLog)
    webSocketService.disconnect()
  }
}
</script>

<template>
  <main class="flex flex-col">
    <flow-header
      :is-running="isRunning"
      :display-log="displayLog"
      @toggle-log="toggleLog"
      @toggle-web-socket="toggleWebSocket"
    />
    <flow-header
      :is-running="isRunning"
      :display-log="displayLog"
      @toggle-log="toggleLog"
      @toggle-web-socket="toggleWebSocket"
    />
    <flow-log :show="displayLog" />
    <div v-if="!displayLog" class="mt-2 h-[calc(100vh-6rem)] w-[calc(100vw-18rem)]" @drop="onDrop">
      <vue-flow
        v-model:nodes="nodes"
        v-model:edges="edges"
        @dragover="onDragOver($event as DragEvent)"
        @dragleave="onDragLeave"
        @edge-update="onEdgeChange"
      >
        <template #node-default="customNodeProps">
          <flow-node v-bind="customNodeProps" />
        </template>
        <template #edge-default="edgeProps">
          <flow-edge v-bind="edgeProps" />
        </template>
        <background />
      </vue-flow>
    </div>
  </main>
</template>
