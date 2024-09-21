import { useVueFlow } from '@vue-flow/core'
import { ref, watch } from 'vue'

let nodeId = 0
let draggedNode: any = null

function setNode(node: any) {
  draggedNode = node
}

function getNode() {
  return draggedNode
}

function getId() {
  return `nodeCounter-${nodeId++}`
}

const state = {
  draggedType: ref(null),
  isDragOver: ref(false),
  isDragging: ref(false)
}

export default function useDragAndDrop() {
  const { addNodes, screenToFlowCoordinate, onNodesInitialized, updateNode } = useVueFlow()
  const { draggedType, isDragOver, isDragging } = state

  watch(isDragging, (dragging) => {
    document.body.style.userSelect = dragging ? 'none' : ''
  })

  // Update any to node types
  function onDragStart(event: DragEvent, device: any) {
    if (event.dataTransfer) {
      setNode(device)
      event.dataTransfer.setData('application/vueflow', 'node')
      event.dataTransfer.effectAllowed = 'move'
    }

    isDragging.value = true
    document.addEventListener('drop', onDragEnd)
  }

  function onDragOver(event: DragEvent) {
    event.preventDefault()

    if (draggedType.value) isDragOver.value = true
  }

  function onDragLeave() {
    isDragOver.value = false
  }

  function onDragEnd() {
    isDragging.value = false
    isDragOver.value = false
    draggedType.value = null
    document.removeEventListener('drop', onDragEnd)
  }

  function onDrop(event: DragEvent) {
    const position = screenToFlowCoordinate({
      x: event.clientX,
      y: event.clientY
    })

    const nodeId = getId()
    const node = getNode()

    // update to reflect our node type
    const newNode = {
      id: nodeId,
      position,
      data: { label: node },
      style: {
        backgroundColor: 'transparent',
        border: 'none',
        padding: '0',
        width: 'fit-content'
      }
    }

    const { off } = onNodesInitialized(() => {
      updateNode(nodeId, (node) => ({
        position: {
          x: node.position.x - node.dimensions.width / 2,
          y: node.position.y - node.dimensions.height / 2
        }
      }))
      off()
    })
    addNodes(newNode)
  }

  return {
    draggedType,
    isDragOver,
    isDragging,
    onDragStart,
    onDragLeave,
    onDragOver,
    onDrop
  }
}
