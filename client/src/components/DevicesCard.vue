<script setup lang="ts">
import { inject, ref, type Ref } from 'vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import '@mdi/font/css/materialdesignicons.css'
import EditPen from '@/icons/EditPen.vue'
import RightArrow from '@/icons/RightArrow.vue'
import type { DeviceType } from '../types/DeviceTypes'
import { useRouter } from 'vue-router'

const props = defineProps<{
  deviceType: DeviceType
}>()

const router = useRouter()

// const showDevices = ref(false)

// const toggleDevices = () => {
//   showDevices.value = !showDevices.value
// }

const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>(
  'updateDeviceTypes',
  () => {}
)

const editDeviceType = ref<DeviceType | null>(null)

const editDeviceClass = (deviceType: DeviceType) => {
  editDeviceType.value = { ...deviceType }
  showEditDeviceTypeForm.value = true
}

const cancelEditDeviceType = () => {
  editDeviceType.value = null
  showEditDeviceTypeForm.value = false
}

const updateDeviceType = () => {
  if (!editDeviceType.value) return

  const updatedDeviceTypes = deviceTypes.value.map((deviceType) => {
    if (deviceType.name === props.deviceType.name) {
      return { ...editDeviceType.value!, name: editDeviceType.value!.name || '' }
    }
    return deviceType
  })
  updateDeviceTypes(updatedDeviceTypes)
  editDeviceType.value = null
  showEditDeviceTypeForm.value = false
}

const navigateToDevice = (deviceName: string) => {
  const currentPath = router.currentRoute.value.fullPath
  router.push(`${currentPath}/${deviceName}`)
}

const showEditDeviceTypeForm = ref(false)
</script>

<template>
  <div class="h-40 w-[25rem] rounded-md bg-secondary-50 p-3 dark:bg-accent-700" style="z-index: 1">
    <!-- usikker på om jeg trenger z-indeks her -->
    <div :class="['flex items-center justify-between']">
      <h2 class="px-2 text-xl font-semibold">{{ deviceType.name }}</h2>
      <BaseButton
        @click="editDeviceClass(deviceType)"
        variant="outline"
        class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <EditPen />
      </BaseButton>
    </div>
    <div class="mt-1 flex">
      <label
        class="m-2 flex w-10 content-start justify-center rounded-lg text-white-100"
        :class="{
          'bg-ble': deviceType.connectionType === 'BLE',
          'bg-wifi': deviceType.connectionType === 'WiFi',
          'bg-ade': deviceType.connectionType === 'ADE'
        }"
      >
        {{ deviceType.connectionType }}
      </label>
      <label class="m-2 w-fit rounded-xl border-2 border-[#6B8AFA] bg-[#E6EBFE] px-2">
        {{
          deviceType.devices?.length === 1
            ? '1 device'
            : `${deviceType.devices?.length || 0}  devices`
        }}
      </label>
    </div>
    <BaseButton
      variant="outline"
      class="ml-auto mt-3 flex w-fit gap-2 rounded-lg border-0 bg-secondary-50 shadow-none dark:bg-accent-700"
      @click="navigateToDevice(deviceType.name)"
    >
      See devices <RightArrow />
    </BaseButton>
  </div>
  <form
    class="absolute left-[50%] top-[50%] z-10 flex w-96 translate-x-[-50%] translate-y-[-50%] transform flex-col gap-6 rounded-xl bg-white-100 p-4 pt-6 shadow-md"
    v-if="showEditDeviceTypeForm && editDeviceType"
  >
    <h2 class="text-lg font-semibold">Edit - Device Type</h2>
    <div class="flex flex-col gap-1">
      <label for="name" class="text-md">Device type name</label>
      <BaseInputField v-model="editDeviceType.name" label="Name" name="name" placeholder="" />
    </div>
    <div class="flex flex-col gap-1">
      <label for="connection-type" class="text-md">Connection type</label>
      <select
        name="connection-type"
        class="rounded-lg border border-accent-600 bg-primary-200 p-2"
        v-model="editDeviceType.connectionType"
      >
        <option value="" disabled>Select connection type</option>
        <option value="BLE">BLE</option>
        <option value="WiFi">WiFi</option>
        <option value="ADE">ADE</option>
      </select>
    </div>
    <div class="mt-6 flex justify-between gap-6">
      <BaseButton variant="outline" @click="cancelEditDeviceType"> Cancel </BaseButton>
      <BaseButton @click="updateDeviceType"> Update </BaseButton>
    </div>
  </form>
  <div
    v-if="showEditDeviceTypeForm"
    class="fixed inset-0 bg-[#000000] opacity-30"
    style="z-index: 2"
  ></div>
</template>
