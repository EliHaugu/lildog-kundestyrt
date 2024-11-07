import type { Flow, Flows } from '../types/FlowType'

const API_BASE_URL = 'http://localhost:8000/data_manager/api'

export default {
  // Get all flows
  async getFlows(): Promise<Flows> {
    const response = await fetch(`${API_BASE_URL}/flows`)
    if (!response.ok) {
      throw new Error(`Error fetching flows: ${response.statusText}`)
    }
    return await response.json()
  },

  //Fetch a flow by ID
  async getFlow(id: string): Promise<Flow> {
    const response = await fetch(`${API_BASE_URL}/flows/${id}`)
    if (!response.ok) {
      throw new Error(`Error fetching flow: ${response.statusText}`)
    }
    return await response.json()
  },

  // Create a new flow
  async createFlow(flowData: Flow): Promise<Flow> {
    const response = await fetch(`${API_BASE_URL}/flows/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(flowData)
    })
    if (!response.ok) {
      throw new Error(`Error creating flow: ${response.statusText}`)
    }
    return await response.json()
  },

  // Delete a flow
  async deleteFlow(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/flows/${id}/`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      throw new Error(`Error deleting flow: ${response.statusText}`)
    }
  },

  // update a flow
  async updateFlow(id: string, flowData: Partial<Flow>): Promise<Flow> {
    // Use Partial<Flow> if only some fields are updated
    const response = await fetch(`${API_BASE_URL}/flows/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(flowData)
    })
    if (!response.ok) {
      throw new Error(`Error updating flow: ${response.statusText}`)
    }
    return await response.json()
  }
}
