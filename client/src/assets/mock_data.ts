import type { Device, DeviceType } from '@/types/DeviceTypes'
import type { CustomNode } from '@/types/NodeType'
import { stripNodeStyles } from '@/utils/stripNodeStyles'

export const listItems = [
  {
    id: '1',
    name: 'Test button activates backend and light',
    link: ''
  },
  {
    id: '2',
    name: 'Test light switches',
    link: ''
  },
  {
    id: '3',
    name: 'Test GPS location tracker turns on',
    link: ''
  }
]

export const headerItems = [
  {
    id: 1,
    name: 'Devices',
    link: 'devices'
  }
]

export const logItems = [
  {
    id: 1,
    name: 'Device 1',
    log: [
      '2021-07-01T00:00:00.000Z',
      '2021-07-01T00:00:01.000Z',
      '2021-07-01T00:00:02.000Z',
      '2021-07-01T00:00:03.000Z',
      '2021-07-01T00:00:04.000Z',
      '2021-07-01T00:00:05.000Z',
      '2021-07-01T00:00:06.000Z',
      '2021-07-01T00:00:07.000Z',
      '2021-07-01T00:00:08.000Z',
      '2021-07-01T00:00:09.000Z',
      '2021-07-01T00:00:10.000Z',
      '2021-07-01T00:00:11.000Z',
      '2021-07-01T00:00:12.000Z'
    ]
  },
  {
    id: 2,
    name: 'Device 2',
    log: ['2021-07-01T00:00:00.000Z']
  },
  {
    id: 3,
    name: 'Device 3',
    log: [
      '2021-07-01T00:00:00.000Z',
      '2021-07-01T00:00:09.000Z',
      '2021-07-01T00:00:10.000Z',
      '2021-07-01T00:00:11.000Z'
    ]
  },
  {
    id: 4,
    name: 'Device 4',
    log: [
      '2021-07-01T00:00:00.000Z',
      '2021-07-01T00:00:01.000Z',
      '2021-07-01T00:00:07.000Z',
      '2021-07-01T00:00:08.000Z',
      '2021-07-01T00:00:09.000Z'
    ]
  },
  {
    id: 5,
    name: 'Device 5',
    log: [
      '2021-07-01T00:00:00.000Z',
      '2021-07-01T00:00:01.000Z',
      '2021-07-01T00:00:02.000Z',
      '2021-07-01T00:00:03.000Z',
      '2021-07-01T00:00:04.000Z'
    ]
  }
]

export const devices: CustomNode[] = [
  {
    id: '1',
    data: { label: 'Button Press', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '2',
    data: { label: 'Backend Updated', connection: 'ADE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '3',
    data: { label: 'Driver Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '4',
    data: { label: 'Light Turned On', connection: 'WiFi' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '5',
    data: { label: 'Button Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '1',
    data: { label: 'Button Press', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '2',
    data: { label: 'Backend Updated', connection: 'ADE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '3',
    data: { label: 'Driver Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '4',
    data: { label: 'Light Turned On', connection: 'WiFi' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '5',
    data: { label: 'Button Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '1',
    data: { label: 'Button Press', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '2',
    data: { label: 'Backend Updated', connection: 'ADE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '3',
    data: { label: 'Driver Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '4',
    data: { label: 'Light Turned On', connection: 'WiFi' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '5',
    data: { label: 'Button Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  },
  {
    id: '5',
    data: { label: 'Button Signal', connection: 'BLE' },
    position: { x: 0, y: 0 },
    style: stripNodeStyles
  }
]

export const mock_devices: Device[] = [
  {
    id: 1,
    name: 'Device 1',
    deviceType: 'Halsbånd',
    connectionType: 'ble',
    connectionId: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 2,
    name: 'Device 2',
    deviceType: 'Halsbånd',
    connectionType: 'ade',
    connectionId: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 3,
    name: 'Device 3',
    deviceType: 'HundeChip',
    connectionType: 'wifi',
    connectionId: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 4,
    name: 'Device 4',
    deviceType: 'GPS-tracker',
    connectionType: 'ble',
    connectionId: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  }
]

export const mock_device_types: DeviceType[] = [
  {
    name: 'Halsbånd',
    connectionType: 'BLE',
    devices: mock_devices.filter((device) => device.deviceType === 'Halsbånd')
  },
  {
    name: 'HundeChip',
    connectionType: 'ADE',
    devices: mock_devices.filter((device) => device.deviceType === 'HundeChip')
  },
  {
    name: 'GPS-tracker',
    connectionType: 'WiFi',
    devices: mock_devices.filter((device) => device.deviceType === 'GPS-tracker')
  }
]
