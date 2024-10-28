<script setup lang="ts">
import type { Device } from '@/types/DeviceTypes'
import { onMounted, ref } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import DeviceInstance from '@/components/devices/DeviceInstance.vue'
import PlusIcon from '@/icons/PlusIcon.vue'
import {
  createDevice,
  fetchDevices,
  updateDevice,
  deleteDevice as removeDevice
} from '@/services/DevicesService'
import ChevronRightIcon from '@/icons/ChevronRightIcon.vue'

const devices = ref<Device[]>([])

onMounted(() => {
  fetchDevices().then((res) => {
    devices.value = res as unknown as Device[]
  })
})

const newDevice = (device: Device) => {
  devices.value.push(device)
  createDevice(device)
}

const editDevice = (id: number, device: Device) => {
  const index = devices.value.findIndex((d) => d.id === id)
  devices.value[index] = device
  updateDevice(id, device)
}

const deleteDevice = (id: number) => {
  devices.value = devices.value.filter((device) => device.id !== id)
  removeDevice(id)
}
</script>

<template>
  <main class="pb-8 pr-4">
    <div class="flex flex-col gap-2">
      <div class="flex items-center gap-2">
        <router-link
          to="/devices"
          class="rounded-md px-2 py-1 text-xl font-semibold hover:bg-accent-800 hover:text-white-100"
          >Device Types</router-link
        >
        <chevron-right-icon />
        <h1 class="text-xl font-semibold">{{ $route.fullPath }}</h1>
      </div>

      <div class="z-20 flex justify-start gap-6">
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Connection type:</p>
          <!--  <p
            class="m-2 flex w-10 content-start justify-center rounded-lg text-white-100"
            :class="{
              'bg-ble': deviceType.connectionType === 'BLE',
              'bg-wifi': deviceType.connectionType === 'WiFi',
              'bg-ade': deviceType.connectionType === 'ADE'
            }"
          >
            {{ deviceType.connectionType }}
        </p> -->
        </div>
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Number of devices:</p>
          <p
            class="m-2 w-fit rounded-xl border-2 border-[#6B8AFA] bg-accent-600 px-2 text-white-100"
          >
            {{ devices?.length === 1 ? '1 device' : `${devices?.length || 0}  devices` }}
          </p>
        </div>
      </div>
      <div class="flex flex-col gap-2">
        <div class="flex items-center justify-between gap-6">
          <div class="z-20 flex w-full items-center justify-start gap-3 text-xl font-semibold">
            <h2 class="w-12">ID</h2>
            <h2 class="w-64">Device instance name</h2>
            <h2 class="w-12">Status</h2>
          </div>
          <base-button
            class="w-40 justify-between rounded-md"
            @click="
              () => {
                newDevice({
                  id: devices.length + 1,
                  device_id: `Test New Device ${devices.length + 1}`,
                  category: 1
                })
              }
            "
          >
            Add device <plus-icon />
          </base-button>
        </div>
        <div class="flex flex-col gap-2">
          <device-instance
            v-for="device in devices"
            :key="device.id"
            :device="device"
            @edit-device="editDevice(device.id, device)"
            @delete-device="deleteDevice(device.id)"
          />
        </div>
      </div>
    </div>
  </main>
</template>
