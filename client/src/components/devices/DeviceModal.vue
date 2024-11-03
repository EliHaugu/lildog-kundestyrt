<script setup lang="ts">
import BaseModal from '../common/BaseModal.vue'
import BaseInputField from '../common/BaseInputField.vue'
import type { Device } from '@/types/DeviceTypes'
import { defineProps, ref } from 'vue'

defineEmits(['submit'])
const props = defineProps({
  id: {
    type: String,
    required: true
  },
  submit: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  device: {
    type: Object as () => Device,
    required: false
  }
})

const deviceModel = ref({
  device_id: props.device?.device_id || '',
  category: props.device?.category.toString(),
  connection_ids: {
    adb_device_id: props.device?.connection_ids.adb_device_id,
    serial_number: props.device?.connection_ids.serial_number
  },
  communication_ids: {
    mac_address: props.device?.communication_ids.mac_address
  }
})
</script>

<template>
  <base-modal
    :id="id"
    :title="title"
    :submitButtonText="submit"
    @submit="$emit('submit', deviceModel)"
  >
    <base-input-field v-model="deviceModel.device_id" label="Name" name="name" placeholder="" />
    <base-input-field
      v-model="deviceModel.category"
      label="Category"
      name="category"
      placeholder=""
      type="number"
    />
    <base-input-field
      v-model="deviceModel.connection_ids.adb_device_id"
      label="ADB Device ID"
      name="adb_device_id"
      placeholder=""
    />
    <base-input-field
      v-model="deviceModel.connection_ids.serial_number"
      label="Serial Number"
      name="serial_number"
      placeholder=""
    />
    <base-input-field
      v-model="deviceModel.communication_ids.mac_address"
      label="MAC Address"
      name="mac_address"
      placeholder=""
    />
  </base-modal>
</template>
