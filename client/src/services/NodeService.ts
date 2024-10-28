// services/NodeService.ts
const API_BASE_URL = 'http://localhost:8000/data_manager/api'

export default {
  async getNodes() {
    const response = await fetch(`${API_BASE_URL}/nodes/`)
    if (!response.ok) {
      throw new Error('Error fetching nodes')
    }
    return await response.json()
  },

  async getNode(id: number) {
    const response = await fetch(`${API_BASE_URL}/nodes/${id}/`)
    if (!response.ok) {
      throw new Error('Error fetching node')
    }
    return await response.json()
  },

  async createNode(nodeData: any) {
    const response = await fetch(`${API_BASE_URL}/nodes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nodeData)
    })
    if (!response.ok) {
      throw new Error('Error creating node')
    }
    return await response.json()
  },

  async updateNode(id: number, nodeData: { x_pos: number; y_pos: number }) {
    const response = await fetch(`${API_BASE_URL}/nodes/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nodeData)
    })
    if (!response.ok) {
      throw new Error('Error updating node')
    }
    return await response.json()
  },

  async deleteNode(id: number) {
    const response = await fetch(`${API_BASE_URL}/nodes/${id}/`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      throw new Error('Error deleting node')
    }
  }
}
