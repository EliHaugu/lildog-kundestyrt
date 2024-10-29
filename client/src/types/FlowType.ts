type Flow = {
  id: string
  name: string
  status?: string
  combinedData?: string[]
  nodes?: number[]
  edges?: number[]
}

type Flows = Flow[]
export type { Flow, Flows }
