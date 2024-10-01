<script setup lang="ts">
import DevicesCard from '@/components/DevicesCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import type { Device } from '@/types/DeviceTypes'

const deviceTypes = ['ble', 'ade', 'wifi']

const devices: Device[] = [
  {
    id: 1,
    name: 'Device 1',
    type: 'ble',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 2,
    name: 'Device 2',
    type: 'ade',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 3,
    name: 'Device 3',
    type: 'wifi',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 4,
    name: 'Device 4',
    type: 'ble',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  }
]
</script>

<template>
  <main>
    <section class="flex justify-between">
      <form action="" class="w-2/3 flex gap-4">
        <BaseInputField />
        <BaseButton type="submit" class="mr-4">Search Devices</BaseButton>
      </form>
      <BaseButton class="w-fit mr-4">New device type</BaseButton>
    </section>
    <ul class="mr-4 grid grid-cols-1 gap-4">
      <DevicesCard 
        v-for="deviceType in deviceTypes" 
        :key="deviceType" 
        :deviceType="deviceType" 
        :devices="devices.filter(device => device.type === deviceType)" 
      />
    </ul>
  </main>
</template>
