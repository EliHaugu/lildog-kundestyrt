<script setup lang="ts">
// import { MiniMap } from '@vue-flow/minimap'
import FlowHeader from '@/components/flow/FlowHeader.vue'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/utils/useDragAndDrop'

import type { Connection, Edge, GraphEdge, NodeDragEvent } from '@vue-flow/core'
import type { CustomNode } from '@/types/NodeType'

import FlowLog from '@/components/flow/FlowLog.vue'
import FlowNode from '@/components/flow/FlowNode.vue'
import FlowEdge from '@/components/flow/FlowEdge.vue'
import { onMounted, ref, type Ref } from 'vue'
import type { Flow } from '@/types/FlowType'

import { useRoute } from 'vue-router'
import flowService from '@/services/FlowService'
import NodeService from '@/services/NodeService'
import EdgeService from '@/services/EdgeService'

const route = useRoute()
const flowId = route.params.id as string

// state to store nodes, edges and flow
const flow = ref<Flow | null>(null)
const nodes = ref<CustomNode[]>([])
const edges = ref<Edge[]>([])

const { onConnect: vueFlowOnConnect, addEdges, updateEdge } = useVueFlow()
const { onDragOver, onDrop, onDragLeave } = useDragAndDrop()

vueFlowOnConnect(addEdges)

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

const updateNodePosition = async (nodeId: string, position: { x: number; y: number }) => {
  try {
    await NodeService.updateNode(Number(nodeId), {
      x_pos: position.x,
      y_pos: position.y
    })
    console.log(`Node ${nodeId} position updated`)
  } catch (error) {
    console.error(`Error updating node ${nodeId} position:`, error)
  }
}

const onNodeDragStop = (nodeDragEvent: NodeDragEvent) => {
  const { id, position } = nodeDragEvent.node
  updateNodePosition(id, position)
}

const fetchFlow = async () => {
  try {
    // Step 1: Fetch the main flow data
    const response = await flowService.getFlow(flowId)
    flow.value = response
    console.log('Fetching flow data:', response)

    // Step 2: Fetch detailed node data by IDs, handling undefined `nodes`
    const nodeIds: number[] = response.nodes ?? []
    const nodePromises = nodeIds.map((nodeId: number) => NodeService.getNode(nodeId))
    const fetchedNodes = await Promise.all(nodePromises)
    console.log('Fetched nodes:', fetchedNodes)

    // Map fetched nodes to VueFlow format
    nodes.value = fetchedNodes.map((node: any) => ({
      id: node.id.toString(),
      position: { x: node.x_pos, y: node.y_pos },
      data: { label: node.label, type: node.node_type }
    }))

    // Step 3: Fetch detailed edge data by IDs, handling undefined `edges`
    const edgeIds = response.edges ?? [] // Use an empty array if `edges` is undefined
    const edgePromises = edgeIds.map((edgeId: number) => EdgeService.getEdge(edgeId))
    const fetchedEdges = await Promise.all(edgePromises)
    console.log('Fetched edges:', fetchedEdges)

    // Map fetched edges to VueFlow format
    edges.value = fetchedEdges.map((edge: any) => ({
      id: edge.id.toString(),
      source: edge.source.toString(),
      target: edge.target.toString()
    }))
  } catch (error) {
    console.error('Error fetching flow data:', error)
  }
}

const onConnect = async (connection: { source: string; target: string }) => {
  try {
    const newEdge = { source: connection.source, target: connection.target }
    const savedEdge = await EdgeService.createEdge(newEdge)

    if (flow.value) {
      flow.value.edges = [...(flow.value.edges ?? []), savedEdge.id]
      await flowService.updateFlow(flowId, { edges: flow.value.edges })
    }
  } catch (error) {
    console.error('Error creating edge:', error)
  }
}

onMounted(fetchFlow)
</script>

<template>
  <main class="flex flex-col">
    <flow-header
      :display-log="displayLog"
      :nodes="nodes"
      :flow="flow ?? {}"
      pdate:display-log="toggleLog"
    />
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
        @node-drag-stop="onNodeDragStop"
        @connect="onConnect"
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
