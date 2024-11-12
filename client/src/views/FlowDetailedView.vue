<script setup lang="ts">
import FlowHeader from '@/components/flow/FlowHeader.vue'
import { Background } from '@vue-flow/background'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import useDragAndDrop from '@/composables/useDragAndDrop'

import type { Connection, Edge, GraphEdge, NodeDragEvent } from '@vue-flow/core'
import type { CustomNode, ImportNode } from '@/types/NodeType'
import type { Log } from '@/types/WebSocketServiceTypes'
import type { Flow } from '@/types/FlowType'
import type { responseType } from '@/services/TestService'

import FlowLog from '@/components/flow/FlowLog.vue'
import FlowNode from '@/components/flow/FlowNode.vue'
import FlowEdge from '@/components/flow/FlowEdge.vue'
import { onMounted, ref } from 'vue'

import { useRoute } from 'vue-router'
import FlowService from '@/services/FlowService'
import NodeService from '@/services/NodeService'
import EdgeService from '@/services/EdgeService'
import { stripNodeStyles } from '@/utils/stripNodeStyles'
import { webSocketService } from '@/services/WebSocketService'
import { updateNode } from '@/services/NodesService'
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

const toggleLog = () => {
  displayLog.value = !displayLog.value
}

const updateNodePosition = async (nodeId: string, position: { x: number; y: number }) => {
  try {
    const node: CustomNode = nodes.value.find((n) => n.id === nodeId)!
    const exportNode = node.data! as unknown as ImportNode

    exportNode.x_pos = position.x
    exportNode.y_pos = position.y

    await updateNode(Number(nodeId), exportNode)
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

    // Step 2: Fetch detailed node data by IDs, handling undefined `nodes`
    const nodeIds: number[] = response.nodes ?? []
    const nodePromises = nodeIds.map((nodeId: number) => NodeService.getNodeProtocol(nodeId))
    const fetchedNodes = await Promise.all(nodePromises)

    // Map fetched nodes to VueFlow format
    nodes.value = fetchedNodes.map((node: any) => ({
      style: stripNodeStyles,
      id: node.id.toString(),
      position: { x: node.x_pos, y: node.y_pos },
      data: {
        id: node.id, // Including `id` here as expected
        label: node.label,
        device: node.device || null, // Add any additional properties expected in the type
        node_type: node.node_type,
        function: node.function, // Assuming `function` might be required
        testState: 'idle',
        x_pos: node.x_pos,
        y_pos: node.y_pos,
        communicationProtocols: node.communication_protocols
      } as any
    }))

    // Step 3: Fetch detailed edge data by IDs, handling undefined `edges`
    const edgeIds = response.edges ?? [] // Use an empty array if `edges` is undefined
    const edgePromises = edgeIds.map((edgeId: number) => EdgeService.getEdge(edgeId))
    const fetchedEdges = await Promise.all(edgePromises)

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

const runFlow = async () => {
  try {
    const response = (await runTest(flowId)) as responseType
    const updatedNodes = response.results[0].nodes_executed

    // Update the node status based on the test results
    for (const node of updatedNodes) {
      const updatedNode = nodes.value.find((n) => n.id === node.node_id.toString())
      if (updatedNode) {
        // @ts-ignore
        updatedNode.data!.testState = node.status
      }
    }
  } catch (error) {
    console.error('Error running test:', error)
  } finally {
    isRunning.value = false
  }
}

// toggle websocket connection
const toggleWebSocket = () => {
  isRunning.value = !isRunning.value

  if (isRunning.value) {
    runFlow()
    webSocketService.connect(8765)
    webSocketService.subscribe((log: Log) => {
      console.log(log)
    })
  } else {
    webSocketService.unsubscribe((log: Log) => {
      console.log(log)
    })
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
          device: nodeData.data.device || null,
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
      // Remove the node from the frontend state
      nodes.value = nodes.value.filter((node) => node.id !== nodeId)
      flow.value.nodes = flow.value.nodes?.filter((id) => id !== Number(nodeId)) || []

      // Update backend to reflect node removal
      await FlowService.updateFlow(flowId, { nodes: flow.value.nodes })
      console.log(`Node ${nodeId} removed from flow (frontend and backend)`)

      // Remove any edges that are now disconnected
      await deleteDisconnectedEdges()

      console.log('Node and disconnected edges cleanup completed.')
    }
  } catch (error) {
    console.error(`Error removing node ${nodeId} from flow:`, error)
  }
}

const deleteDisconnectedEdges = async () => {
  try {
    if (flow.value) {
      // Retrieve all edge details to ensure backend IDs are accurate
      const edgeIds = flow.value.edges ?? []
      const edgePromises = edgeIds.map((edgeId: number) => EdgeService.getEdge(edgeId))
      const fetchedEdges = await Promise.all(edgePromises)

      // Identify edges with disconnected nodes
      const disconnectedEdges = fetchedEdges.filter((edge) => {
        const sourceExists = flow.value?.nodes?.includes(edge.source)
        const targetExists = flow.value?.nodes?.includes(edge.target)
        return !(sourceExists && targetExists) // Keep only disconnected edges
      })

      // Delete disconnected edges in the backend
      for (const edge of disconnectedEdges) {
        console.log(`Deleting disconnected edge with ID: ${edge.id} from backend`)
        await EdgeService.deleteEdge(edge.id) // Use precise backend ID for deletion
      }

      // Update frontend edge state to remove disconnected edges
      edges.value = edges.value.filter((edge) => {
        const sourceExists = flow.value?.nodes?.includes(Number(edge.source))
        const targetExists = flow.value?.nodes?.includes(Number(edge.target))
        return sourceExists && targetExists
      })

      // Update the flow's edge list with currently connected edges
      flow.value.edges = edges.value.map((edge) => Number(edge.id))
      await FlowService.updateFlow(flowId, { edges: flow.value.edges })

      console.log(`Disconnected edges removed from flow (frontend and backend)`)
    }
  } catch (error) {
    console.error('Error deleting disconnected edges from flow:', error)
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
