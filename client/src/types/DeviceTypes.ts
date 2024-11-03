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
}

type DeviceType = {
  name: string
  connectionType: string
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
