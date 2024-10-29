const API_BASE_URL = 'http://localhost:8000/data_manager/api/categories'

export default {
  async getCategory(id: number) {
    const response = await fetch(`${API_BASE_URL}/${id}/`)
    if (!response.ok) {
      throw new Error('Error fetching node')
    }
    return await response.json()
  }
}
