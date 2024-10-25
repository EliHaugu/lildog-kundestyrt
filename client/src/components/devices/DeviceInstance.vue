<script setup lang="ts">
import { ref } from 'vue'
import type { Device } from '@/types/DeviceTypes'
import CheckIcon from '@/icons/CheckIcon.vue'
import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'

const props = defineProps<{
  device: Device
}>()

const device = ref(props.device)

const emit = defineEmits(['edit-device', 'delete-device'])

const editDevice = () => {
  emit('edit-device', device)
}

const deleteDevice = () => {
  emit('delete-device', device)
}
</script>

<template>
  <div
    class="flex items-center justify-between gap-6 rounded-md px-2 py-1 hover:bg-secondary-50 dark:hover:bg-accent-700"
  >
    <div class="flex items-center justify-start gap-3">
      <p class="w-12">{{ device.id }}</p>
      <p class="w-64">{{ device.name }}</p>
      <div class="w-fit rounded-full bg-success p-1">
        <check-icon />
      </div>
    </div>
    <div class="flex items-center justify-start gap-3">
      <button class="w-fit rounded-lg p-1 hover:bg-accent-500" @click="editDevice">
        <edit-pen />
      </button>
      <button class="w-fit rounded-lg p-1 text-error hover:bg-accent-500" @click="deleteDevice">
        <delete-icon />
      </button>
    </div>
  </div>
</template>
