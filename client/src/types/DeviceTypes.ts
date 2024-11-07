type Device = {
  id: number
  device_id: string
  category: number
  connection_ids: {
    adb_device_id?: string
    serial_number?: string
  }
  communication_ids: {
    mac_address?: string
  }
  connection_ids: {
    adb_device_id?: string
    serial_number?: string
  }
  communication_ids: {
    mac_address?: string
  }
}

type DeviceCategory = {
  id: number
  name: string
  connectionTypes: string[]
  communicationProtocols: string[]
  devices?: Device[]
}

type DeviceModel = {
  device_id: string
  category: string
  connection_ids: {
    adb_device_id: string
    serial_number: string
  }
  communication_ids: {
    mac_address: string
  }
}

export type { Device, DeviceType, DeviceModel }
