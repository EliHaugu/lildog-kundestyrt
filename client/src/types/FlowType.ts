type Flow = {
  id: string
  name: string
  status?: string
  connectionType?: string[]
  communicationProtocol?: string[]
  nodes?: number[]
  edges?: number[]
}

type Flows = Flow[]
export type { Flow, Flows }
