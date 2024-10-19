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

  // Map through the existing deviceTypes and replace the one being edited
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
  // Assuming currentPath is where you are currently, you can get the current path from router
  const currentPath = router.currentRoute.value.fullPath
  router.push(`${currentPath}/${deviceName}`) // Navigate to currentPath + deviceId
}

// const showNewDeviceForm = ref(false)
// const newDeviceName = ref('')
// const newDeviceConnection = ref(props.deviceType.connectionType || '')

// const addNewDevice = () => {
//   if (!newDeviceName.value || !newDeviceConnection.value) {
//     if (!newDeviceName.value) {
//       console.error('Device name is required')
//     }
//     if (!newDeviceConnection.value) {
//       console.error('Device connection is required')
//     }
//     return
//   } else if (
//     deviceTypes.value.some((deviceType) =>
//       deviceType.devices?.some((device) => device.name === newDeviceName.value)
//     )
//   ) {
//     console.error('Device name already exists')
//     return
//   }

//   const newDevice: Device = {
//     id: Date.now(),
//     name: newDeviceName.value,
//     deviceType: props.deviceType.name,
//     connectionType: 'default', // Replace with actual connection type if available
//     connectionId: newDeviceConnection.value,
//     fields: { key: '', value: '' }
//   }

//   const devices = props.deviceType.devices || []

//   updateDeviceTypes(
//     deviceTypes.value.map((deviceType) => {
//       if (deviceType.name === props.deviceType.name) {
//         return {
//           ...deviceType,
//           devices: [...devices, newDevice]
//         }
//       }
//       return deviceType
//     })
//   )

//   showNewDeviceForm.value = false
// }

// const deleteDevice = (device: Device) => {
//   updateDeviceTypes(
//     deviceTypes.value.map((deviceType) => {
//       if (deviceType.name === props.deviceType.name) {
//         return {
//           ...deviceType,
//           devices: deviceType.devices?.filter((d) => d.id !== device.id)
//         }
//       }
//       return deviceType
//     })
//   )
// }

// const response = ref([
//   {
//     id: 1,
//     number: 300,
//     status: 'OK',
//     name: 'Device 1'
//   }
// ])

const showEditDeviceTypeForm = ref(false)

// const testConnection = ref(false)

// const toggleTestConnection = () => {
//   testConnection.value = !testConnection.value
// }

// import { listItems } from '@/assets/mock_data'
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

  <!-- <BaseButton
          variant="outline"
          class="w-fit shadow-none active:bg-accent-700 active:text-white-100"
          @click="showNewDeviceForm = !showNewDeviceForm"
        >
          Add Device
          <i class="mdi mdi-plus p-1 text-xl"></i>
        </BaseButton> -->
  <!-- <BaseButton
          class="w-fit bg-opacity-0 shadow-none"
          variant="secondary"
          @click="toggleDevices"
        >
          <i v-if="showDevices" class="mdi mdi-chevron-up p-1 text-xl"></i>
          <i v-else class="mdi mdi-chevron-down p-1 text-xl"></i>
        </BaseButton> -->

  <!-- <div
      :class="['flex w-full flex-row gap-2 pt-2', showDevices ? 'border-t-2 border-[#d4d4d4]' : '']"
      v-if="showDevices"
    >
      <ul class="w-full">
        <li
          v-for="(device, index) in deviceType.devices"
          :key="device.id"
          class="flex w-full items-center gap-5 rounded-md p-2 hover:cursor-pointer hover:bg-[#e3e3e3]"
        >
          <div>{{ index + 1 }}.</div>
          <div>
            {{ device.name }}
          </div>
          <div
            class="flex w-10 content-start justify-center rounded-lg text-white-100"
            :class="{
              'bg-ble': device.connectionType === 'BLE',
              'bg-wifi': device.connectionType === 'WiFi',
              'bg-ade': device.connectionType === 'ADE'
            }"
          >
            {{ device.connectionType }}
          </div>
          <BaseButton
            variant="secondary"
            class="group ml-auto flex h-12 w-12 items-center justify-center rounded-full border-[#000000] bg-opacity-0 p-0 text-error shadow-none hover:bg-error active:bg-[#9c1c1c]"
          >
            <i
              class="mdi mdi-delete text-lg group-hover:text-white-100 group-active:text-white-100"
              @click="deleteDevice(device)"
            ></i>
          </BaseButton>
        </li>
      </ul>
    </div> -->
  <!-- <form
    class="absolute left-[50%] top-[50%] z-10 flex w-96 translate-x-[-50%] translate-y-[-50%] transform flex-col gap-6 rounded-xl bg-white-100 p-4 pt-6 shadow-md"
    v-if="showNewDeviceForm"
  >
    <h2 class="text-xl font-semibold">Create new - Device</h2>
    <div class="flex flex-col gap-1">
      <label for="name" class="text-md">Device name</label>
      <BaseInputField v-model="newDeviceName" label="Name" name="name" placeholder="" />
    </div>
    <div class="flex flex-col gap-1">
      <label for="connection" class="text-md">Device connection</label>
      <div class="flex w-full justify-between gap-3">
        <select
          name="connection"
          class="h-fit w-full rounded-lg border border-accent-600 bg-primary-200 p-2"
          v-model="newDeviceConnection"
        >
          <option
            v-for="deviceType in deviceTypes"
            :key="deviceType.name"
            :value="deviceType.connectionType"
          >
            {{ deviceType.connectionType }}
          </option>
        </select>
        <BaseButton @click="toggleTestConnection">Test</BaseButton>
      </div>
      <div class="flex w-fit justify-between gap-3">
        <label>Response:</label>
        <label class="font-bold" v-if="testConnection" for="response">
          {{ response[0].number }} {{ response[0].status }}
        </label>
      </div>
    </div>
    <select name="Add to board" class="h-12 rounded-xl border border-accent-700 px-2">
      <option value="" disabled selected>Select Board</option>
      <option v-for="item in listItems" :key="item.id">
        {{ item.name }}
      </option>
    </select>
    <div class="mt-6 flex justify-between gap-6">
      <BaseButton variant="outline" @click="showNewDeviceForm = false"> Cancel </BaseButton>
      <BaseButton @click="addNewDevice"> Add Device </BaseButton>
    </div>
  </form> -->
  <!-- <div v-if="showNewDeviceForm" class="fixed inset-0 bg-[#000000] opacity-30"></div> -->
</template>
