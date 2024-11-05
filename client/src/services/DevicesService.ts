import type { Device } from '@/types/DeviceTypes'

/**
 * Fetch all devices.
 * @returns list of devices received from the server
 */
export async function fetchDevices(): Promise<Device[]> {
  const requestOptions = {
    method: 'GET'
  }

  const response = await fetch(`http://127.0.0.1:8000/data_manager/api/devices/`, requestOptions)

  if (!response.ok) {
    console.error('Failed to fetch devices')
    return []
  }

  return await response.json()
}

/**
 * Fetch devices by category name.
 * @param categoryName - Name of the category to fetch devices from
 * @returns list of devices received from the server
 */
export async function fetchDevicesByCategory(categoryId: number): Promise<Device[]> {
  const requestOptions = {
    method: 'GET'
  }

  const url = `http://127.0.0.1:8000/data_manager/api/devices/?category_id=${encodeURIComponent(
    categoryId
  )}`

  const response = await fetch(url, requestOptions)

  if (!response.ok) {
    console.error(`Failed to fetch devices for category: ${categoryId}`)
    return []
  }

  return await response.json()
}

export async function fetchDevice(id: number): Promise<Device | null> {
  const requestOptions = {
    method: 'GET'
  }
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/data_manager/api/devices/${id}/`,
      requestOptions
    )
    if (!response.ok) {
      throw new Error(`Error fetching device with ID ${id}: ${response.statusText}`)
    }
    const device: Device = await response.json()
    return device
  } catch (error) {
    console.error('Error in fetchDevice:', error)
    return null // Return null if there's an error
  }
}

/**
 * @param device device to create, containing all the needed fields
 * @returns true if response is 200/OK, signifying that the device was created successfully
 */
export async function createDevice(device: Device): Promise<Boolean> {
  if (device.connection_ids.adb_device_id === '') {
    delete device.connection_ids.adb_device_id
  }
  if (device.connection_ids.serial_number === '') {
    delete device.connection_ids.serial_number
  }
  if (device.communication_ids.mac_address === '') {
    delete device.communication_ids.mac_address
  }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: device.device_id,
      category: device.category, // Should be the category ID
      connection_ids: device.connection_ids,
      communication_ids: device.communication_ids
    })
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices/`, requestOptions)).ok
}

/**
 * @param device device to delete,
 * @returns true if response is 200/OK, signifying that the device was deleted successfully
 */
export async function deleteDevice(id: number): Promise<Boolean> {
  const requestOptions = {
    method: 'DELETE'
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices/${id}/`, requestOptions)).ok
}

/**
 * @param device device to update, with the new values
 * @returns true if response is 200/OK, signifying that the device was updated successfully
 */
export async function updateDevice(id: number, device: Device): Promise<Boolean> {
  const requestOptions = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: device.device_id,
      category: device.category
    })
  }
  return (await fetch(`http://127.0.0.1:8000/data_manager/api/devices/${id}/`, requestOptions)).ok
}
