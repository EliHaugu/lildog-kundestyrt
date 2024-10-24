import type { Device } from '@/types/DeviceTypes'

/**
 * @param category category to fetch devices from
 * @returns list of devices following the Device type
 */
export async function fetchDevices(category: string): Promise<Device[]> {
  const requestOptions = {
    method: 'GET'
  }
  console.log('fetching devices')

  const response = await fetch(
    `http://127.0.0.1:8000/data_manager/api/devices`,
    requestOptions
  ).then((response) => {
    return response.json()
  })

  console.log('response', response)

  return response
}

/**
 * @param device device to create
 * @returns true if the device was created successfully
 */
export async function createDevice(device: Device): Promise<Boolean> {
  const requestOptions = {
    method: 'POST',
    body: JSON.stringify(device)
  }

  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices`, requestOptions)).ok
}

/**
 *
 * @param device device to delete
 * @returns true if the device was deleted successfully
 */
export async function deleteDevice(device: Device): Promise<Boolean> {
  const requestOptions = {
    method: 'DELETE'
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices`, requestOptions)).ok
}

/**
 *
 * @param device device to update
 * @returns true if the device was updated successfully
 */
export async function updateDevice(device: Device): Promise<Boolean> {
  const requestOptions = {
    method: 'PATCH'
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices`, requestOptions)).ok
}
