<script setup lang="ts">
import FlowHeader from '@/components/flow/FlowHeader.vue'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/composables/useDragAndDrop'

import type { Connection, Edge, GraphEdge, NodeDragEvent } from '@vue-flow/core'
import type { CustomNode } from '@/types/NodeType'

import FlowLog from '@/components/flow/FlowLog.vue'
import FlowNode from '@/components/flow/FlowNode.vue'
import FlowEdge from '@/components/flow/FlowEdge.vue'
import { nextTick, onMounted, ref } from 'vue'
import type { Flow } from '@/types/FlowType'

import { useRoute } from 'vue-router'
import FlowService from '@/services/FlowService'
import NodeService from '@/services/NodeService'
import EdgeService from '@/services/EdgeService'
import { stripNodeStyles } from '@/utils/stripNodeStyles'
import { webSocketService } from '@/services/WebSocketService'
import type { Log } from '@/types/WebSocketServiceTypes'

import { runTest } from '@/services/TestService'

const route = useRoute()
const flowId = route.params.id as string

// state to store nodes, edges and flow
const flow = ref<Flow | null>(null)
const nodes = ref<CustomNode[]>([])
const edges = ref<Edge[]>([])

const { onConnect: vueFlowOnConnect, addEdges, updateEdge, onNodesChange } = useVueFlow()
const { onDragOver, onDragLeave } = useDragAndDrop()

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
const isRunning = ref(false)

const handleNewLog = (log: Log) => {
  console.log('new log', log)
}

// toggle log display
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
    const response = await FlowService.getFlow(flowId)
    flow.value = response
    console.log('Fetching flow data:', response)

    // Step 2: Fetch detailed node data by IDs, handling undefined `nodes`
    const nodeIds: number[] = response.nodes ?? []
    const nodePromises = nodeIds.map((nodeId: number) => NodeService.getNodeProtocol(nodeId))
    const fetchedNodes = await Promise.all(nodePromises)
    console.log('Fetched nodes:', fetchedNodes)

    // Map fetched nodes to VueFlow format
    nodes.value = fetchedNodes.map((node: any) => ({
      style: stripNodeStyles,
      id: node.id.toString(),
      position: { x: node.x_pos, y: node.y_pos },
      data: {
        id: node.id, // Including `id` here as expected
        label: node.label,
        device: node.device, // Add any additional properties expected in the type
        node_type: node.node_type,
        function: node.function, // Assuming `function` might be required
        x_pos: node.x_pos,
        y_pos: node.y_pos,
        communicationProtocols: node.communication_protocols
      } as any
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
      await FlowService.updateFlow(flowId, { edges: flow.value.edges })
    }
  } catch (error) {
    console.error('Error creating edge:', error)
  }
}

onMounted(fetchFlow)
// toggle websocket connection
const toggleWebSocket = () => {
  isRunning.value = !isRunning.value

  if (isRunning.value) {
    runTest(flowId[0])
    webSocketService.connect(8765)
    webSocketService.subscribe(handleNewLog)
  } else {
    webSocketService.unsubscribe(handleNewLog)
    webSocketService.disconnect()
  }
}

const addNodeToFlow = async (nodeData: any, position: { x: number; y: number }) => {
  try {
    // Ensure flow exists
    if (flow.value) {
      // Add the node with full details to the nodes array
      nodes.value.push({
        id: nodeData.id,
        position,
        style: stripNodeStyles,
        data: {
          id: nodeData.id,
          label: nodeData.data.label,
          node_type: nodeData.node_type,
          device: nodeData.data.device,
          function: nodeData.data.function,
          x_pos: position.x, // Save the position for persistence
          y_pos: position.y
        } as any
      })

      // Save the updated position in the database
      await NodeService.updateNode(Number(nodeData.id), {
        x_pos: position.x,
        y_pos: position.y
      })

      // Update the flow's node list with the new node ID if it’s not already present
      if (!flow.value.nodes?.includes(Number(nodeData.id))) {
        flow.value.nodes = [...(flow.value.nodes ?? []), Number(nodeData.id)]
        await FlowService.updateFlow(flowId, { nodes: flow.value.nodes })
      }
      fetchFlow()
    }
  } catch (error) {
    console.error('Error adding existing node to flow:', error)
  }
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()

  // Parse the full node data from the drag event
  const nodeData = JSON.parse(event.dataTransfer?.getData('node') || '{}')
  const dropPosition = { x: event.offsetX, y: event.offsetY }

  if (nodeData.id) {
    addNodeToFlow(nodeData, dropPosition) // Add node to the flow with position
  }
}

const removeNodeFromFlow = async (nodeId: string) => {
  try {
    if (flow.value) {
      // Step 1: Remove the node from the flow (frontend only)
      nodes.value = nodes.value.filter((node) => node.id !== nodeId)
      flow.value.nodes = flow.value.nodes?.filter((id) => id !== Number(nodeId)) || []

      // Step 2: Identify edges that are now disconnected and need to be deleted from the backend
      const disconnectedEdges = edges.value.filter((edge) => {
        const sourceInFlow = flow.value?.nodes?.includes(Number(edge.source)) ?? false
        const targetInFlow = flow.value?.nodes?.includes(Number(edge.target)) ?? false
        return !(sourceInFlow && targetInFlow)
      })

      // Step 3: Delete disconnected edges from the backend
      for (const edge of disconnectedEdges) {
        if (!isNaN(Number(edge.id))) {
          console.log(`Deleting disconnected edge with ID: ${edge.id} from backend`)
          await EdgeService.deleteEdge(Number(edge.id))
        } else {
          console.warn(`Skipping deletion for invalid edge ID: ${edge.id}`)
        }
      }

      // Step 4: Remove disconnected edges from the frontend state
      edges.value = edges.value.filter((edge) => {
        const sourceInFlow = flow.value?.nodes?.includes(Number(edge.source)) ?? false
        const targetInFlow = flow.value?.nodes?.includes(Number(edge.target)) ?? false
        return sourceInFlow && targetInFlow
      })

      // Step 5: Update the backend to reflect the flow's current nodes and edges without the removed node and edges
      flow.value.edges =
        flow.value.edges?.filter((edgeId) =>
          edges.value.some((edge) => String(edge.id) === String(edgeId))
        ) || []
      await FlowService.updateFlow(flowId, { nodes: flow.value.nodes, edges: flow.value.edges })

      console.log(
        `Node ${nodeId} removed from the flow and its disconnected edges deleted from backend`
      )
    }
  } catch (error) {
    console.error(`Error removing node ${nodeId} and deleting disconnected edges from flow:`, error)
  }
}

// Intercept deletion in `onNodesChange`
onNodesChange(async (changes) => {
  for (const change of changes) {
    if (change.type === 'remove') {
      // Call `removeNodeFromFlow` for database update
      await removeNodeFromFlow(change.id)
    }
  }
})
</script>

<template>
  <main class="flex flex-col">
    <flow-header
      :flow="flow || {}"
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
        @node-drag-stop="onNodeDragStop"
        @connect="onConnect"
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
