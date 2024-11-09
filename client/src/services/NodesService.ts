import type { ImportNode, BaseNode as Node } from '@/types/NodeType'

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/data_manager/api/nodes/`

/**
 * @returns list of nodes received from the server
 */
export async function fetchNodes(): Promise<Node[]> {
  const requestOptions = {
    method: 'GET'
  }

  const response = await fetch(API_BASE_URL, requestOptions).then((response) => {
    return response.json()
  })
  const baseResponse = []
  for (let i = 0; i < response.length; i++) {
    baseResponse.push({
      id: response[i].id,
      position: {
        x: response[i].x_pos,
        y: response[i].y_pos
      },
      data: response[i]
    })
  }
  return baseResponse as Node[]
}

/**
 * @param node node to create, containing all the needed fields
 * @returns true if response is 200/OK, signifying that the node was created successfully
 */

export async function createNode(node: Partial<ImportNode>): Promise<Boolean> {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(node)
  }
  return (await fetch(API_BASE_URL, requestOptions)).ok
}

/**
 * @param node node to delete,
 * @returns true if response is 200/OK, signifying that the node was deleted successfully
 */
export async function deleteNode(id: number): Promise<Boolean> {
  const requestOptions = {
    method: 'DELETE'
  }
  return (await fetch(`${API_BASE_URL}${id}/`, requestOptions)).ok
}

/**
 * @param node node to update, with the new values
 * @returns true if response is 200/OK, signifying that the node was updated successfully
 */
export async function updateNode(id: number, node: ImportNode): Promise<Boolean> {
  const requestOptions = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(node)
  }
  return (await fetch(`${API_BASE_URL}${id}/`, requestOptions)).ok
}
