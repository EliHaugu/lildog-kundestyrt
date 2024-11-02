import type { CustomNode, CustomAssertNode } from '@/types/NodeType'
import axios from 'axios'

const API_BASE_URL = '/api/nodes'

export function createApiAssertNode(
  label: string,
  apiUrl: string,
  expectedApiResponse: string,
  apiPayload: string
): CustomAssertNode {
  return {
    id: generateUniqueId(),
    data: {
      label,
      assertionMethod: 'API',
      apiUrl,
      expectedApiResponse,
      apiPayload
    },
    position: { x: 0, y: 0 }
  }
}

export function createUartAssertNode(
  label: string,
  expectedUARTLog: string,
  timeout: number
): CustomAssertNode {
  return {
    id: generateUniqueId(),
    data: {
      label,
      assertionMethod: 'UART',
      expectedUARTLog,
      timeout
    },
    position: { x: 0, y: 0 }
  }
}

export function validateAssertNode(node: CustomAssertNode): boolean {
  if (node.data?.assertionMethod === 'API') {
    if (!node.data.apiUrl || !node.data.expectedApiResponse) {
      console.error("API assertion nodes require 'apiUrl' and 'expectedApiResponse'.")
      return false
    }
  } else if (node.data?.assertionMethod === 'UART') {
    if (!node.data.expectedUARTLog || node.data.timeout === undefined) {
      console.error("UART assertion nodes require 'expectedUARTLog' and 'timeout'.")
      return false
    }
  }
  return true
}

export async function saveAssertNode(node: CustomAssertNode): Promise<any> {
  if (!validateAssertNode(node)) {
    return Promise.reject(new Error('Node validation failed'))
  }
  try {
    const response = await axios.post(`${API_BASE_URL}/save`, node)
    return response.data
  } catch (error) {
    console.error('Failed to save node:', error)
    throw error
  }
}

export async function getAssertNodes(): Promise<CustomNode[]> {
  try {
    const response = await axios.get(`${API_BASE_URL}/list`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch nodes:', error)
    throw error
  }
}

function generateUniqueId(): string {
  return Math.random().toString(36).substr(2, 9)
}

async function submitApiCheck(
  nodeId: number | string,
  apiUrl: string,
  apiPayload: string,
  expectedResponse: string
) {
  try {
    const response = await fetch(`/check_assertion/${nodeId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        api_url: apiUrl,
        api_payload: apiPayload,
        expected_response: expectedResponse
      })
    })
    const data = await response.json()
    document.getElementById('api-assert-feedback')!.innerText = data.result
  } catch (error) {
    document.getElementById('api-assert-feedback')!.innerText = 'Error: ' + error
  }
}

async function submitUartCheck(nodeId: number | string, uartLogString: string, timeout: number) {
  try {
    const response = await fetch(`/check_assertion/${nodeId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        expected_uart_log: uartLogString,
        timeout: timeout
      })
    })
    const data = await response.json()
    document.getElementById('uart-assert-feedback')!.innerText = data.result
  } catch (error) {
    document.getElementById('uart-assert-feedback')!.innerText = 'Error: ' + error
  }
}
