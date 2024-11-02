<script setup lang="ts">
import type { Device } from '@/types/DeviceTypes'
import CheckIcon from '@/icons/CheckIcon.vue'
import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'

import BaseButton from '../common/BaseButton.vue'
import BaseInputField from '../common/BaseInputField.vue'
import BaseModal from '../common/BaseModal.vue'

import {
  updateDevice,
  deleteDevice as removeDevice
} from '@/services/DevicesService'
import { ref } from 'vue'

const emit = defineEmits(['update'])
const props = defineProps<{
  device: Device
}>()

const openModal = () => {
  ;(document.getElementById('editDeviceModal'+props.device.id) as HTMLDialogElement).showModal()
}

const editDeviceModel = ref({
  name: props.device.device_id,
  category: props.device.category.toString()
})

const editDevice = () => {
  const device = {
    id: props.device.id,
    device_id: editDeviceModel.value.name,
    category: Number(editDeviceModel.value.category)
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
      <p class="w-12">{{ device.id }}</p>
      <p class="w-64">{{ device.device_id }}</p>
      <div class="w-fit rounded-full bg-success p-1">
        <check-icon />
      </div>
    </div>
    <div class="flex items-center justify-start gap-3">
      <base-button variant="icon" class="rounded-md" @click="openModal">
        <edit-pen class="dark:fill-white-100" />
      </base-button>
      <base-button variant="icon" class="rounded-md" @click="deleteDevice">
        <delete-icon class="fill-error" />
      </base-button>
    </div>
    <base-modal :id="'editDeviceModal'+device.id" title="Edit Device" submitButtonText="Add" @submit="editDevice">
      <base-input-field v-model="editDeviceModel.name" label="Name" name="name" placeholder="" />
      <base-input-field
        v-model="editDeviceModel.category"
        label="Category"
        name="category"
        placeholder=""
        type="number"
      />
    </base-modal>
  </div>
</template>
