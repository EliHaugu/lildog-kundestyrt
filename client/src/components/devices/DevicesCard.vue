<script setup lang="ts">
import { computed, inject, ref, type Ref } from 'vue'
import BaseButton from '../common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseModal from '../common/BaseModal.vue'
import '@mdi/font/css/materialdesignicons.css'
import EditPen from '@/icons/EditPen.vue'
import RightArrow from '@/icons/RightArrow.vue'
import type { DeviceType } from '../../types/DeviceTypes'
import { useRouter } from 'vue-router'

const props = defineProps<{
  deviceType: DeviceType
}>()

const router = useRouter()

const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>(
  'updateDeviceTypes',
  () => {}
)

const editDeviceType = ref<DeviceType | null>(null)

const connectionTypes = computed(() => {
  return [...new Set(deviceTypes.value.map((deviceType) => deviceType.connectionType))]
})

const editDeviceClass = (deviceType: DeviceType) => {
  editDeviceType.value = { ...deviceType }
  ;(
    document.getElementById(`editDeviceTypeForm${deviceType.name}`) as HTMLDialogElement
  ).showModal()
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
  <div class="h-40 w-[25rem] rounded-md bg-secondary-50 p-3 dark:bg-accent-700">
    <div :class="['flex items-center justify-between']">
      <h2 class="px-2 text-xl font-semibold">{{ deviceType.name }}</h2>
      <base-button
        @click="editDeviceClass(deviceType)"
        variant="outline"
        class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <edit-pen />
      </base-button>
    </div>
    <div class="mt-1 flex">
      <label
        class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-ble': deviceType.connectionType === 'BLE',
          'bg-wifi': deviceType.connectionType === 'WiFi',
          'bg-ade': deviceType.connectionType === 'ADE'
        }"
      >
        {{ deviceType.connectionType }}
      </label>
      <label
        class="m-2 w-fit rounded-xl border-2 border-accent-500 bg-accent-700 px-2 text-white-100"
      >
        {{
          deviceType.devices?.length === 1
            ? '1 device'
            : `${deviceType.devices?.length || 0}  devices`
        }}
      </label>
    </div>
    <base-button
      variant="outline"
      class="ml-auto mt-3 flex w-fit gap-2 rounded-lg border-0 bg-secondary-50 shadow-none dark:bg-accent-700"
      @click="navigateToDevice(deviceType.name)"
    >
      See devices <right-arrow />
    </base-button>
  </div>

  <base-modal
    :id="'editDeviceTypeForm' + deviceType.name"
    submitButtonText="Update"
    title="Edit Device Type"
    @submit="updateDeviceType"
  >
    <base-input-field label="Name" name="name" placeholder="" />
    <base-input-field
      label="Connection type"
      name="connection-type"
      placeholder=""
      type="select"
      :options="connectionTypes"
    />
  </base-modal>
</template>
