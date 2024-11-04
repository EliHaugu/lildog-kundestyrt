import { useVueFlow } from '@vue-flow/core'
import { ref, watch } from 'vue'
import type { BaseNode as Node } from '@/types/NodeType'
import { stripNodeStyles } from '../utils/stripNodeStyles'

let draggedNode: Node
let uniqueId = 0

function setNode(node: Node) {
  draggedNode = node
  draggedNode.id = uniqueId.toString()
}

function getNode() {
  return draggedNode
}

function getId() {
  return `nodeCounter-${uniqueId++}`
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

  function onDragStart(event: DragEvent, device: Node) {
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

    const node = getNode()
    const id = getId()
    const newNode: Node = {
      ...node,
      id,
      position
    }

    const { off } = onNodesInitialized(() => {
      updateNode(id, (node) => ({
        position: {
          x: node.position.x - node.dimensions.width / 2,
          y: node.position.y - node.dimensions.height / 2
        },
        style: stripNodeStyles
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
