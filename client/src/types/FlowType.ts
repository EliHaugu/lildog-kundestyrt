import type { Edge } from '@vue-flow/core'
import type { CustomNode } from './NodeType'

type Flow = {
  id: string
  name: string
  status?: string
  connectionTypes?: string[]
  nodes?: number[]
  edges?: number[]
}

type Flows = Flow[]
export type { Flow, Flows }
