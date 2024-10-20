<script setup lang="ts">
import { ref, inject, computed } from 'vue'
import type { Ref } from 'vue'
import DevicesCard from '@/components/DevicesCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import type { DeviceType } from '@/types/DeviceTypes'

const showNewDeviceTypeForm = ref(false)

const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>(
  'updateDeviceTypes',
  () => {}
)
const newDeviceTypeName = ref('')
const newDeviceTypeConnection = ref('')
const searchQuery = ref('')

const addNewDeviceType = () => {
  if (!newDeviceTypeName.value || !newDeviceTypeConnection.value) {
    if (!newDeviceTypeName.value) {
      console.error('Device type name is required')
    }
    if (!newDeviceTypeConnection.value) {
      console.error('Device type connection is required')
    }
    return
  }

  const newDeviceType: DeviceType = {
    name: newDeviceTypeName.value,
    connectionType: newDeviceTypeConnection.value
  }

  updateDeviceTypes([...deviceTypes.value, newDeviceType])

  showNewDeviceTypeForm.value = false
  newDeviceTypeName.value = ''
  newDeviceTypeConnection.value = ''
}

const filteredDeviceTypes = computed(() => {
  return deviceTypes.value.filter((deviceType) =>
    deviceType.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <main class="flex flex-col gap-6">
    <section class="flex gap-2 h-10">
      <h1 class="p-2 pt-1 text-2xl font-semibold">Configure devices</h1>
      <form action="" class="ml-auto flex flex-grow gap-4">
        <base-input-field
          v-model="searchQuery"
          placeholder="Search device types"
          class="rounded-lg"
        />
      </form>
      <base-button class="mr-4 w-fit items-center rounded-lg" @click="showNewDeviceTypeForm = true">
        New device type
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </section>
    <ul class="mr-4 flex flex-wrap gap-4">
      <devices-card
        v-for="deviceType in filteredDeviceTypes"
        :key="deviceType.name"
        :deviceType="deviceType"
      />
    </ul>
    <!-- page for making new device type -->
    <form
      class="absolute left-[50%] top-[50%] z-10 flex w-96 translate-x-[-50%] translate-y-[-50%] transform flex-col gap-6 rounded-xl bg-primary-100 p-4 pt-6 shadow-md"
      v-if="showNewDeviceTypeForm"
    >
      <h2 class="text-lg font-semibold">Create new - Device Type</h2>
      <div className="flex flex-col gap-1">
        <label for="name" class="text-md">Device type name</label>
        <base-input-field v-model="newDeviceTypeName" label="Name" name="name" placeholder="" />
      </div>
      <div class="flex flex-col gap-1">
        <label for="connection-type" class="text-md">Connection type</label>
        <select
          name="connection-type"
          class="rounded-lg border border-accent-600 bg-primary-200 p-2"
          v-model="newDeviceTypeConnection"
        >
          <option value="" disabled selected>Select connection type</option>
          <option
            v-for="deviceType in deviceTypes"
            :key="deviceType.name"
            :value="deviceType.connectionType"
          >
            {{ deviceType.connectionType }}
          </option>
        </select>
      </div>
      <div class="mt-6 flex justify-between gap-2">
        <base-button class="rounded-md flex-grow justify-center" variant="outline" @click="showNewDeviceTypeForm = false">Cancel</base-button>
        <base-button class="rounded-md flex-grow justify-center" @click="addNewDeviceType">Create</base-button>
      </div>
    </form>
    <div v-if="showNewDeviceTypeForm" class="fixed inset-0 bg-[#000000] opacity-30"></div>
  </main>
</template>
