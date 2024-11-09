const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/data_manager/api`

export default {
  // Fetch all edges
  async getEdges() {
    const response = await fetch(`${API_BASE_URL}/edges/`)
    if (!response.ok) {
      throw new Error('Error fetching edges')
    }
    return await response.json()
  },

  // Fetch a specific edge by ID
  async getEdge(id: number) {
    const response = await fetch(`${API_BASE_URL}/edges/${id}/`)
    if (!response.ok) {
      throw new Error('Error fetching edge')
    }
    return await response.json()
  },

  // Create a new edge
  async createEdge(edgeData: any) {
    const response = await fetch(`${API_BASE_URL}/edges/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(edgeData)
    })
    if (!response.ok) {
      throw new Error('Error creating edge')
    }
    return await response.json()
  },

  // Update an edge by ID
  async updateEdge(id: number, edgeData: any) {
    const response = await fetch(`${API_BASE_URL}/edges/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(edgeData)
    })
    if (!response.ok) {
      throw new Error('Error updating edge')
    }
    return await response.json()
  },

  // Delete an edge by ID
  async deleteEdge(id: number) {
    const response = await fetch(`${API_BASE_URL}/edges/${id}/`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      throw new Error('Error deleting edge')
    }
  }
}
