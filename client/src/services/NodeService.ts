const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/data_manager/api`

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
  },

  async getNodeProtocol(id: number) {
    const response = await fetch(`${API_BASE_URL}/nodes/${id}/`)
    if (!response.ok) {
      throw new Error('Error fetching node')
    }
    const nodeData = await response.json()
    let communication_protocols: any[] = []

    console.log('HELLO', nodeData.device)

    if (nodeData.device) {
      // Fetch the device associated with this node
      const deviceResponse = await fetch(`${API_BASE_URL}/devices/${nodeData.device}/`) // Assuming nodeData.device gives you the device ID
      if (!deviceResponse.ok) {
        throw new Error('Error fetching device')
      }
      const deviceData = await deviceResponse.json()

      // Fetch the category associated with this device
      const categoryResponse = await fetch(`${API_BASE_URL}/categories/${deviceData.category}/`) // Assuming deviceData.category gives you the category ID
      if (!categoryResponse.ok) {
        throw new Error('Error fetching category')
      }
      const categoryData = await categoryResponse.json()
      communication_protocols = categoryData.communication_protocols
    }

    return {
      id: nodeData.id,
      device: nodeData.device,
      label: nodeData.label,
      node_type: nodeData.node_type,
      function: nodeData.function,
      x_pos: nodeData.x_pos,
      y_pos: nodeData.y_pos,
      communication_protocols: communication_protocols || []
    }
  }
}
