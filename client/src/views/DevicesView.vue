<template>
  <main class="flex flex-col gap-6">
    <section class="flex h-10 gap-2">
      <h1 class="p-2 pt-1 text-2xl font-semibold flex-shrink-0">Configure devices</h1>
      <form action="" class="ml-auto flex-grow ">
        <base-input-field
          v-model="searchQuery"
          placeholder="Search device types"
          class="rounded-lg flex-shrink min-w-0"
        />
      </form>
      <base-button @click="openModal" class="flex w-48 flex-shrink-0 items-center gap-2">
        New device type
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </section>
    <ul class="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
      <devices-card
        v-for="deviceType in filteredDeviceTypes"
        :key="deviceType.name"
        :deviceType="deviceType"
      />
    </ul>
    <base-modal
      id="newDeviceTypeModal"
      title="Create Device Type"
      submit-button-text="Create"
      @submit="addNewDeviceType"
    >
      <base-input-field v-model="newDeviceTypeName" label="Name" name="name" placeholder="" />
      <base-input-field
        v-model="newDeviceTypeConnection"
        label="Connection type"
        name="connection-type"
        placeholder=""
        type="select"
        :options="connectionTypes"
      />
    </base-modal>
  </main>
</template>

<script setup lang="ts">
import { ref, inject, computed } from 'vue'
import type { Ref } from 'vue'
import DevicesCard from '@/components/devices/DevicesCard.vue'
import BaseButton from '../components/common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseModal from '../components/common/BaseModal.vue'
import type { DeviceType } from '@/types/DeviceTypes'

const openModal = () => {
  ;(document.getElementById('newDeviceTypeModal') as HTMLDialogElement).showModal()
}

const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>(
  'updateDeviceTypes',
  () => {}
)
const newDeviceTypeName = ref('')
const newDeviceTypeConnection = ref('')
const searchQuery = ref('')

const connectionTypes = computed(() => {
  return [...new Set(deviceTypes.value.map((deviceType) => deviceType.connectionType))]
})

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

  newDeviceTypeName.value = ''
  newDeviceTypeConnection.value = ''
}

const filteredDeviceTypes = computed(() => {
  return deviceTypes.value.filter((deviceType) =>
    deviceType.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>
