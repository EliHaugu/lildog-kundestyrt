import type { Node } from '@vue-flow/core'

export type CustomData = {
  label: string
  connection?: string
  flowId?: string
}

export type CustomNode = Node<CustomData>
