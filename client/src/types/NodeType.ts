import type { Node } from '@vue-flow/core'

export type CustomData = {
  label: string
  connection?: string
  flowId?: string
  type?: string
  testState: string
  fields?: { uuid?: string; action?: string; assertion?: string }
}

export type CustomNode = Node<CustomData>
