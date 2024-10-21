<script setup lang="ts">
// import { MiniMap } from '@vue-flow/minimap'
import FlowHeader from '@/components/flow/FlowHeader.vue'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/utils/useDragAndDrop'

import type { Connection, Edge, GraphEdge } from '@vue-flow/core'
import type { CustomNode } from '@/types/NodeType'

import FlowLog from '@/components/flow/FlowLog.vue'
import FlowNode from '@/components/flow/FlowNode.vue'
import FlowEdge from '@/components/flow/FlowEdge.vue'
import { ref, type Ref } from 'vue'
import { stripNodeStyles } from '@/utils/stripNodeStyles'
import type { Flows } from '@/types/FlowType'

import { inject, computed } from 'vue'
import { useRoute } from 'vue-router'

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

const toggleLog = () => {
  displayLog.value = !displayLog.value
}
</script>

<template>
  <main class="flex flex-col">
    <flow-header :display-log="displayLog" @update:display-log="toggleLog" />
    <flow-log :show="displayLog" />
    <div
      v-show="!displayLog"
      class="mt-2 h-[calc(100vh-8rem)] w-[calc(100vw-18rem)]"
      @drop="onDrop"
    >
      <vue-flow
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
      </vue-flow>
    </div>
  </main>
</template>
