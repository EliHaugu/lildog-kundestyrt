<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import type { DeviceCategory } from '@/types/DeviceTypes';

import BaseButton from '@/components/common/BaseButton.vue';
import BaseInputField from '@/components/common/BaseInputField.vue';
import BaseModal from '@/components/common/BaseModal.vue';

import EditPen from '@/icons/EditPen.vue';
import RightArrow from '@/icons/RightArrow.vue';

import { updateCategory, deleteCategory as deleteCategoryService } from '@/services/CategoryService';

const props = defineProps<{
  deviceCategory: DeviceCategory;
}>();

const emit = defineEmits(['updated', 'deleted', 'click']);

// State for managing edit modal and edit data
const isEditModalVisible = ref(false);
const editedCategory = ref<DeviceCategory>({ ...props.deviceCategory });

// Static options for dropdowns
const connectionTypes = ['adb', 'uart'];
const communicationProtocols = ['wifi', 'bluetooth', 'lte'];

// Function to open the edit modal with the current category data
const openEditModal = () => {
  editedCategory.value = { ...props.deviceCategory }; // Deep copy to avoid direct mutation
  isEditModalVisible.value = true;
};

// Function to update the category
const saveCategoryChanges = async () => {
  const updatedData = {
    connectionTypes: editedCategory.value.connectionTypes,
    communicationProtocols: editedCategory.value.communicationProtocols,
  };

  const success = await updateCategory(editedCategory.value.id, updatedData);
  if (success) {
    isEditModalVisible.value = false;
    emit('updated', editedCategory.value);
  } else {
    console.error('Failed to update device category');
  }
};

// Function to delete the category
const deleteCategory = async () => {
  const confirmed = confirm(`Are you sure you want to delete ${props.deviceCategory.name}?`);
  if (confirmed) {
    const success = await deleteCategoryService(props.deviceCategory.id);
    if (success) {
      emit('deleted', props.deviceCategory.id);
    } else {
      console.error('Failed to delete device category');
    }
  }
};

// Router instance
const router = useRouter();

// Function to navigate to the devices path
const navigateToDevices = () => {
  router.push(`/categories/${props.deviceCategory.id}`);
};

// Rest of your script
</script>

<template>
  <div class="h-fit rounded-md bg-secondary-50 p-3 dark:bg-accent-700">
    <div class="flex items-center justify-between">
      <h2 class="px-2 text-xl font-semibold">{{ deviceCategory.name }}</h2>
      <base-button
        @click="openEditModal"
        variant="outline"
        class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <edit-pen />
      </base-button>
    </div>

    <div class="mt-1 flex flex-wrap">
      <div
        v-for="connectionType in deviceCategory.connectionTypes"
        :key="connectionType"
        class="m-1 px-2 py-1 text-xs rounded-full text-white-100"
        :class="{
          'bg-blue-500': connectionType === 'adb',
          'bg-green-500': connectionType === 'uart'
        }"
      >
        {{ connectionType }}
      </div>

      <div
        v-for="protocol in deviceCategory.communicationProtocols"
        :key="protocol"
        class="m-1 px-2 py-1 text-xs rounded-full text-white-100"
        :class="{
          'bg-purple-500': protocol === 'wifi',
          'bg-red-500': protocol === 'bluetooth',
          'bg-yellow-500': protocol === 'lte'
        }"
      >
        {{ protocol }}
      </div>
    </div>

    <div class="mt-2">
      <span class="text-sm text-gray-700 dark:text-gray-300">
        {{ deviceCategory.devices?.length || 0 }} devices
      </span>
    </div>

    <base-button
      variant="outline"
      class="ml-auto mt-3 flex w-fit gap-2 rounded-lg border-0 bg-secondary-50 shadow-none dark:bg-accent-700"
      @click="navigateToDevices"
    >
      See devices <right-arrow />
    </base-button>

    <base-button
      variant="outline"
      class="ml-auto mt-1 flex w-fit gap-2 rounded-lg border-0 bg-red-500 text-white shadow-none"
      @click="deleteCategory"
    >
      Delete
    </base-button>
  </div>

  <!-- Edit Modal -->
  <base-modal
    v-if="isEditModalVisible"
    id="editDeviceCategoryForm"
    submitButtonText="Update"
    title="Edit Device Category"
    @submit="saveCategoryChanges"
    @close="isEditModalVisible = false"
  >
    <base-input-field v-model="editedCategory.name" label="Name" name="name" placeholder="" disabled />
    <base-input-field
      v-model="editedCategory.connectionTypes[0]"
      label="Connection type"
      name="connection-type"
      placeholder=""
      inputType="select"
      :options="connectionTypes"
    />
    <base-input-field
      v-model="editedCategory.communicationProtocols[0]"
      label="Communication protocol"
      name="communication-protocol"
      placeholder=""
      inputType="select"
      :options="communicationProtocols"
    />
  </base-modal>
</template>
