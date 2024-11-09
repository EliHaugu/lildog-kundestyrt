<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Device, DeviceCategory } from '@/types/DeviceTypes'

import BaseButton from '@/components/common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseModal from '@/components/common/BaseModal.vue'

import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'
import RightArrow from '@/icons/RightArrow.vue'

import { updateCategory, deleteCategory as deleteCategoryService } from '@/services/CategoryService'
import { fetchDevicesByCategory } from '@/services/DevicesService'

const props = defineProps<{
  deviceCategory: DeviceCategory
}>()

const emit = defineEmits(['updated', 'deleted', 'click'])

const devices = ref<Device[]>([])
const numDevices = ref(0)

onMounted(async () => {
  const fetchedDevices = await fetchDevicesByCategory(props.deviceCategory.id)
  devices.value = fetchedDevices
  numDevices.value = fetchedDevices.length
})

// State for managing edit modal and edit data
const isEditModalVisible = ref(false)
const editedCategory = ref<DeviceCategory>({ ...props.deviceCategory })

// Static options for dropdowns
// const connectionTypes = ['adb', 'uart'];
// const communicationProtocols = ['wifi', 'bluetooth', 'lte'];

// Function to open the edit modal with the current category data
const editDeviceCategory = () => {
  editedCategory.value = { ...props.deviceCategory }
  ;(
    document.getElementById(`editDeviceCategoryForm${props.deviceCategory.id}`) as HTMLDialogElement
  ).showModal()
}

// Function to update the category
const saveCategoryChanges = async () => {
  const updatedData = {
    category_name: editedCategory.value.category_name,
    connection_types: editedCategory.value.connection_types,
    communication_protocols: editedCategory.value.communication_protocols
  }

  const success = await updateCategory(editedCategory.value.id, updatedData)
  if (success) {
    isEditModalVisible.value = false
    emit('updated', editedCategory.value)
  } else {
    console.error('Failed to update device category')
  }
}

// Function to delete the category
const deleteCategory = async () => {
  const confirmed = confirm(
    `Are you sure you want to delete ${props.deviceCategory.category_name}?`
  )
  if (confirmed) {
    const success = await deleteCategoryService(props.deviceCategory.id)
    if (success) {
      emit('deleted', props.deviceCategory.id)
    } else {
      console.error('Failed to delete device category')
    }
  }
}

// Router instance
const router = useRouter()

// Function to navigate to the devices path
const navigateToDevices = () => {
  router.push(`/categories/${props.deviceCategory.id}`)
}

// Rest of your script
</script>

<template>
  <div class="flex h-fit flex-col gap-0 rounded-md bg-secondary-50 p-3 dark:bg-accent-700">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">{{ deviceCategory.category_name }}</h2>
      <div>
        <base-button
          @click.stop="editDeviceCategory"
          variant="outline"
          class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
          aria-label="Edit category"
        >
          <edit-pen />
        </base-button>
        <base-button
          variant="outline"
          class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
          @click="deleteCategory"
          aria-label="Delete category"
        >
          <delete-icon />
        </base-button>
      </div>
    </div>

    <div class="mt-1 flex flex-wrap gap-2">
      <div
        v-for="connectionType in deviceCategory.connection_types"
        :key="connectionType"
        class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-ble': connectionType === 'uart',
          'bg-ade': connectionType === 'adb'
        }"
      >
        {{ connectionType }}
      </div>

      <div
        v-for="protocol in deviceCategory.communication_protocols"
        :key="protocol"
        class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-ble': protocol === 'ble',
          'bg-wifi': protocol === 'wifi',
          'bg-ade': protocol === 'lte'
        }"
      >
        {{ protocol }}
      </div>

      <p class="m-2 w-fit rounded-xl bg-accent-600 px-2 text-white-100">
        {{ devices?.length === 1 ? '1 device' : `${devices?.length || 0} devices` }}
      </p>
    </div>

    <base-button
      variant="outline"
      class="ml-auto mt-3 flex w-fit gap-2 rounded-lg border-0 bg-secondary-50 shadow-none dark:bg-accent-700"
      @click="navigateToDevices"
      aria-label="See devices"
    >
      See devices <right-arrow />
    </base-button>
  </div>

  <!-- Edit Modal -->
  <base-modal
    :id="'editDeviceCategoryForm' + deviceCategory.id"
    submitButtonText="Update"
    title="Edit Device Category"
    @submit="saveCategoryChanges"
  >
    <base-input-field
      v-model="editedCategory.category_name"
      label="Name"
      name="name"
      placeholder=""
    />
    <!-- <base-input-field
      v-model="editedCategory.connectionTypes"
      label="Connection type"
      name="connection-type"
      placeholder=""
      inputType="select"
      :options="connectionTypes"
    /> -->
    <!-- <base-input-field
      v-model="editedCategory.communicationProtocols"
      label="Communication protocol"
      name="communication-protocol"
      placeholder=""
      inputType="select"
      :options="communicationProtocols"
    /> -->
  </base-modal>
</template>
