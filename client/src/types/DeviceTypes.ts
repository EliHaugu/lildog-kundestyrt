type Device = {
  id: number
  device_id: string
  category: string
}

type DeviceType = {
  name: string
  connectionType: string
  devices?: Device[]
}

export type { Device, DeviceType }
