import type { Node } from '@vue-flow/core'

export type CustomData = {
  label: string
  connection?: string
  flowId?: string
  type?: string
  testState?: string
  fields?: { uuid?: string; action?: string; assertion?: string }
}

export type CustomAssertData = CustomData &
  (
    | {
        assertionMethod: 'API'
        apiUrl: string
        apiPayload: string
        expectedApiResponse: string
      }
    | {
        assertionMethod: 'UART'
        expectedUARTLog: string
        timeout: number
      }
  )

export type CustomNode = Node<CustomData>

export type CustomAssertNode = Node<CustomAssertData>
