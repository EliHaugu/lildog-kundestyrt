type Device = {
  id: number
  name: string
  deviceType: string
  connectionType: string
  connectionId: string
  fields: {
    key: string
    value: string
  }
}

type DeviceType = {
  name: string
  connectionType: string
  devices?: Device[]
}

export type { Device, DeviceType }
