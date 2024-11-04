import type { DeviceCategory } from '@/types/DeviceTypes'

/**
 * @returns list of categories (DeviceCategories) received from the server
 */
export async function fetchCategories(): Promise<DeviceCategory[]> {
  const requestOptions = {
    method: 'GET'
  }

  const response = await fetch(
    `http://127.0.0.1:8000/data_manager/api/categories`,
    requestOptions
  ).then((response) => {
    return response.json()
  })

  return response.map(mapCategory)
}

/**
 * @param category category (DeviceCategory) to create, containing all the needed fields
 * @returns true if response is 200/OK, signifying that the category was created successfully
 */
export async function createCategory(
  category: Partial<{ category_name: string; connection_types: string[] }>
): Promise<Boolean> {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(category)
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/`, requestOptions)).ok
}

/**
 * @param id ID of the category to delete
 * @returns true if response is 200/OK, signifying that the category was deleted successfully
 */
export async function deleteCategory(id: number): Promise<Boolean> {
  const requestOptions = {
    method: 'DELETE'
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/${id}/`, requestOptions))
    .ok
}

/**
 * @param id ID of the category to update
 * @param category updated category object
 * @returns true if response is 200/OK, signifying that the category was updated successfully
 */
export async function updateCategory(
  id: number,
  category: Partial<DeviceCategory>
): Promise<Boolean> {
  const requestOptions = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(mapToBackendModel(category))
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/${id}/`, requestOptions))
    .ok
}

const mapCategory = (category: {
  id: number
  category_name: string
  connection_types: string[]
  communication_protocols: string[]
}): DeviceCategory => {
  return {
    id: category.id, // Include the ID
    name: category.category_name,
    connectionTypes: category.connection_types,
    communicationProtocols: category.communication_protocols
  }
}

const mapToBackendModel = (
  category: Partial<DeviceCategory>
): Partial<{
  category_name: string
  connection_types: string[]
  communication_protocols: string[]
}> => {
  return {
    category_name: category.name,
    connection_types: category.connectionTypes,
    communication_protocols: category.communicationProtocols
  }
}
