<script setup lang="ts">
import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'

import BaseButton from '../common/BaseButton.vue'
import DeviceModal from '@/components/devices/DeviceModal.vue'
import type { Device, DeviceModel } from '@/types/DeviceTypes'
import { updateDevice, deleteDevice as removeDevice } from '@/services/DevicesService'

const emit = defineEmits(['update'])
const props = defineProps<{
  device: Device
}>()

const openModal = () => {
  ;(document.getElementById('editDeviceModal' + props.device.id) as HTMLDialogElement).showModal()
}

const editDevice = (editDeviceModel: DeviceModel) => {
  const device = {
    id: props.device.id,
    device_id: editDeviceModel.device_id,
    category: parseInt(editDeviceModel.category),
    connection_ids: {
      adb_device_id: editDeviceModel.connection_ids.adb_device_id,
      serial_number: editDeviceModel.connection_ids.serial_number
    },
    communication_ids: {
      mac_address: editDeviceModel.communication_ids.mac_address
    }
  }
  updateDevice(props.device.id, device).then(() => {
    emit('update')
  })
}

const deleteDevice = () => {
  removeDevice(props.device.id).then(() => {
    emit('update')
  })
}
</script>

<template>
  <div
    class="flex items-center justify-between gap-6 rounded-md px-2 py-1 hover:bg-secondary-50 dark:hover:bg-accent-700"
  >
    <div class="flex items-center justify-start gap-3">
      <p class="w-12" aria-label="ID">{{ device.id }}</p>
      <p class="w-64" aria-label="Name">{{ device.device_id }}</p>
    </div>
    <div class="flex items-center justify-start gap-3">
      <base-button aria-label="Edit device" variant="icon" class="rounded-md" @click="openModal">
        <edit-pen class="dark:fill-white-100" />
      </base-button>
      <base-button aria-label="Delete device" variant="icon" class="rounded-md" @click="deleteDevice">
        <delete-icon class="fill-error" />
      </base-button>
    </div>
    <device-modal
      :id="'editDeviceModal' + device.id"
      :device="device"
      submit="Save"
      title="Edit Device"
      @submit="editDevice"
    />
  </div>
</template>
