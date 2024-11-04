<script setup lang="ts">
import type { DeviceType } from '@/types/DeviceTypes';
import { ref, inject, computed, onMounted } from 'vue';
import type { Ref } from 'vue';

import DevicesCard from '@/components/devices/DevicesCard.vue';
import BaseButton from '../components/common/BaseButton.vue';
import BaseInputField from '@/components/common/BaseInputField.vue';
import BaseModal from '../components/common/BaseModal.vue';

import { fetchCategories, createCategory, deleteCategory, updateCategory } from '@/services/CategoryService';

const openModal = () => {
  (document.getElementById('newDeviceTypeModal') as HTMLDialogElement).showModal();
};

const deviceTypes = ref<DeviceType[]>([]);
const newDeviceTypeName = ref('');
const newDeviceTypeConnection = ref('');
const newDeviceTypeCommunication = ref('');
const searchQuery = ref('');

// Fetch categories on component mount
onMounted(async () => {
  const response = await fetchCategories();
  deviceTypes.value = mapDeviceTypes(response);
});

const connectionTypes = ['adb', 'uart'];
const communicationProtocols = ['wifi', 'bluetooth', 'lte'];

const mapDeviceTypes = (deviceTypes: { category_name: string, connection_types: string[], communication_protocols: string[] }[]): DeviceType[] => {
  const mappedDeviceTypes: DeviceType[] = [];
  
  for (const deviceType of deviceTypes) {
    mappedDeviceTypes.push({
      name: deviceType.category_name,
      connectionType: deviceType.connection_types[0],
      communicationProtocols: deviceType.communication_protocols
    });
  }

  return mappedDeviceTypes;
};

// Add new category (DeviceType) and send to server
const addNewDeviceType = async () => {
  if (!newDeviceTypeName.value || !newDeviceTypeConnection.value || !newDeviceTypeCommunication.value) {
    if (!newDeviceTypeName.value) {
      console.error('Device type name is required');
    }
    if (!newDeviceTypeConnection.value) {
      console.error('Device type connection is required');
    }
    if (!newDeviceTypeCommunication.value) {
      console.error('Device type communication protocol is required');
    }
    return;
  }

  const newDeviceType: { category_name: string, connection_types: string[], communication_protocols: string[] } = {
    category_name: newDeviceTypeName.value,
    connection_types: [newDeviceTypeConnection.value],
    communication_protocols: [newDeviceTypeCommunication.value]
  };

  // Send the new device type to the server
  const created = await createCategory(newDeviceType);
  console.log('created', created);
  if (created) {
    deviceTypes.value = mapDeviceTypes(await fetchCategories()); // Refresh the list after adding
    newDeviceTypeName.value = '';
    newDeviceTypeConnection.value = '';
  } else {
    console.error('Failed to create device type');
  }
};

// Delete category
const deleteDeviceType = async (deviceType: DeviceType) => {
  const confirmed = confirm(`Are you sure you want to delete ${deviceType.name}?`);
  if (confirmed) {
    const deleted = await deleteCategory(deviceType.name);
    if (deleted) {
      deviceTypes.value = mapDeviceTypes(await fetchCategories()); // Refresh list after deletion
    } else {
      console.error('Failed to delete device type');
    }
  }
};

// Update category (Example: Could be used in an edit modal)
const updateDeviceType = async (name: string, updatedDeviceType: Partial<DeviceType>) => {
  const updated = await updateCategory(name, updatedDeviceType);
  if (updated) {
    deviceTypes.value = mapDeviceTypes(await fetchCategories()); // Refresh list after update
  } else {
    console.error('Failed to update device type');
  }
};

// Filtered device types based on search query
const filteredDeviceTypes = computed(() => {
  return deviceTypes.value.filter((deviceType) =>
    deviceType.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>

<template>
  <main class="flex flex-col gap-6">
    <section class="flex h-10 gap-2">
      <h1 class="flex-shrink-0 p-2 pt-1 text-2xl font-semibold">Device categories</h1>
      <form action="" class="ml-auto flex-grow">
        <base-input-field
          v-model="searchQuery"
          placeholder="Search device types"
          class="flex-shrink rounded-lg"
        />
      </form>
      <base-button @click="openModal" class="flex w-48 flex-shrink-0 items-center gap-2">
        New category
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </section>
    <ul class="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      <devices-card
        v-for="deviceType in filteredDeviceTypes"
        :key="deviceType.name"
        :deviceType="deviceType"
        @delete="deleteDeviceType(deviceType)"
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
      <base-input-field
        v-model="newDeviceTypeCommunication"
        label="Communication protocol"
        name="communication-protocol"
        placeholder=""
        type="select"
        :options="communicationProtocols"
      />w
    </base-modal>
  </main>
</template>
