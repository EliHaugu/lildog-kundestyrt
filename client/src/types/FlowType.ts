type Flow = {
  id: string
  name: string
  status?: string
  connectionType?: string[]
  conmmunicationProtocol?: string[]
  nodes?: number[]
  edges?: number[]
}

type Flows = Flow[]
export type { Flow, Flows }
