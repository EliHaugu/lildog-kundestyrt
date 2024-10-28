type Device = {
  id: number
  device_id: string
  category: number
}

type DeviceType = {
  name: string
  connectionType: string
  devices?: Device[]
}

export type { Device, DeviceType }
