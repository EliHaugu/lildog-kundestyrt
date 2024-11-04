import type { Device, DeviceType } from '@/types/DeviceTypes';

/**
 * @returns list of categories (DeviceTypes) received from the server
 */
export async function fetchCategories(): Promise<{ category_name: string, connection_types: string[], communication_protocols: string[] }[]> {
  const requestOptions = {
    method: 'GET'
  };

  const response = await fetch(`http://127.0.0.1:8000/data_manager/api/categories`, requestOptions).then((response) => {
    return response.json();
  });

  return response;
}

/**
 * @param category category (DeviceType) to create, containing all the needed fields
 * @returns true if response is 200/OK, signifying that the category was created successfully
 */
export async function createCategory(category: Partial<{ category_name: string, connection_types: string[]}>): Promise<Boolean> {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(category)
  };
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/`, requestOptions)).ok;
}

/**
 * @param id ID of the category to delete
 * @returns true if response is 200/OK, signifying that the category was deleted successfully
 */
export async function deleteCategory(name: string): Promise<Boolean> {
  const requestOptions = {
    method: 'DELETE'
  };
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/${name}/`, requestOptions)).ok;
}

/**
 * @param id ID of the category to update
 * @param category updated category object
 * @returns true if response is 200/OK, signifying that the category was updated successfully
 */
export async function updateCategory(name: string, category: Partial<DeviceType>): Promise<Boolean> {
  const requestOptions = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(category)
  };
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/categories/${name}/`, requestOptions)).ok;
}
