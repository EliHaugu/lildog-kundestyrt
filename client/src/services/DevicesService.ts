import type { Device } from '@/types/DeviceTypes'

/**
 * @param category category to fetch devices from
 * @returns list of devices received from the server
 */
export async function fetchDevices(): Promise<Device[]> {
  const requestOptions = {
    method: 'GET'
  }

  const response = await fetch(
    `http://127.0.0.1:8000/data_manager/api/devices`,
    requestOptions
  ).then((response) => {
    return response.json()
  })

  return response
}

export async function fetchDevice(id: number): Promise<Device | null> {
  const requestOptions = {
    method: 'GET',
  };
  try {
    const response = await fetch(`http://127.0.0.1:8000/data_manager/api/devices/${id}/`, requestOptions);
    if (!response.ok) {
      throw new Error(`Error fetching device with ID ${id}: ${response.statusText}`);
    }
    const device: Device = await response.json();
    return device;

  } catch (error) {
    console.error('Error in fetchDevice:', error);
    return null; // Return null if there's an error
  }
}
  

/**
 * @param device device to create, containing all the needed fields
 * @returns true if response is 200/OK, signifying that the device was created successfully
 */
export async function createDevice(device: Device): Promise<Boolean> {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: device.device_id,
      category: device.category
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
