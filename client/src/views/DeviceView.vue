<script setup lang="ts">
import type { Device, DeviceType } from '@/types/DeviceTypes'
import { computed, inject, onMounted, ref, type Ref } from 'vue'
import { useRoute } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import DeviceInstance from '@/components/devices/DeviceInstance.vue'
import PlusIcon from '@/icons/PlusIcon.vue'
import { createDevice, fetchDevices } from '@/services/DevicesService'
import ChevronRightIcon from '@/icons/ChevronRightIcon.vue'
import BaseModal from '@/components/common/BaseModal.vue'

const devices = ref<Device[]>([])
// Inject the device types, and find the device type that matches the current route
const route = useRoute()
const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const deviceType = computed(() => {
  return deviceTypes.value.find((deviceType) => deviceType.name === route.fullPath.split('/').pop())
})

const newDeviceModel = ref({
  name: '',
  category: ''
})

const openModal = () => {
  ;(document.getElementById('newDeviceModal') as HTMLDialogElement).showModal()
}

onMounted(() => {
  fetchDevices().then((res) => {
    devices.value = res as unknown as Device[]
  })
})

const newDevice = () => {
  const device = {
    id: devices.value.length + 1,
    device_id: newDeviceModel.value.name,
    category: parseInt(newDeviceModel.value.category)
  }
  createDevice(device).then((res: Boolean) => {
    if (res) {
      update()
    } else {
      console.error('Failed to create device')
    }
  })
}

const update = () => {
  fetchDevices().then((res) => {
    devices.value = res as unknown as Device[]
  })
}
</script>

<template>
  <main class="pb-8 pr-4">
    <div class="flex h-full flex-col gap-2">
      <div class="flex grow-0 items-center gap-2">
        <router-link
          to="/devices"
          class="rounded-md px-2 py-1 text-xl font-semibold hover:bg-accent-800 hover:text-white-100"
          >Device Types</router-link
        >
        <chevron-right-icon />
        <h1 class="text-xl font-semibold">{{ $route.fullPath.split('/').pop() }}</h1>
      </div>

      <div class="z-20 flex grow-0 justify-start gap-6">
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Connection type:</p>
          <label
            class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
            :class="{
              'bg-ble': deviceType?.connectionType === 'BLE',
              'bg-wifi': deviceType?.connectionType === 'WiFi',
              'bg-ade': deviceType?.connectionType === 'ADE'
            }"
          >
            {{ deviceType?.connectionType }}
          </label>
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
      <div class="flex grow flex-col gap-2 overflow-y-auto">
        <div class="flex grow-0 items-center justify-between gap-6">
          <div class="z-20 flex w-full items-center justify-start gap-3 text-xl font-semibold">
            <h2 class="w-12">ID</h2>
            <h2 class="w-64">Device instance name</h2>
            <h2 class="w-12">Status</h2>
          </div>
          <base-button class="justify-between text-nowrap rounded-md" @click="openModal">
            Add device <plus-icon />
          </base-button>
        </div>
        <div class="flex grow flex-col gap-2 overflow-y-auto">
          <device-instance
            @update="update"
            v-for="device in devices"
            :key="device.id"
            :device="device"
          />
        </div>
      </div>
    </div>
    <base-modal id="newDeviceModal" title="Edit Device" submitButtonText="Save" @submit="newDevice">
      <base-input-field v-model="newDeviceModel.name" label="Name" name="name" placeholder="" />
      <base-input-field
        v-model="newDeviceModel.category"
        label="Category"
        name="category"
        placeholder=""
        type="number"
      />
    </base-modal>
  </main>
</template>
