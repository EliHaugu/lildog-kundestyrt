import type { Node, XYPosition } from '@vue-flow/core'

export type ImportNode = {
  id: number
  label: string
  device: number
  node_type: string
  function: string
  testState?: string
  x_pos?: number
  y_pos?: number
}

export type BaseNode = {
  id: string
  position: XYPosition
  data: ImportNode
}

export type CustomNode = Node<BaseNode>
