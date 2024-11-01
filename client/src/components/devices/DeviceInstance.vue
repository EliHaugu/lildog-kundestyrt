<script setup lang="ts">
import type { Device } from '@/types/DeviceTypes'
import CheckIcon from '@/icons/CheckIcon.vue'
import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'

import BaseButton from '../common/BaseButton.vue'

defineEmits(['edit-device', 'delete-device'])
defineProps<{
  device: Device
}>()
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
      <base-button variant="icon" class="rounded-md" @click="$emit('edit-device')">
        <edit-pen class="dark:fill-white-100" />
      </base-button>
      <base-button variant="icon" class="rounded-md" @click="$emit('delete-device')">
        <delete-icon class="fill-error" />
      </base-button>
    </div>
  </div>
</template>
