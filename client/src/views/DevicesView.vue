<script setup lang="ts">
import { ref, inject } from 'vue'
import type { Ref } from 'vue'
import DevicesCard from '@/components/DevicesCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import type { DeviceType } from '@/types/DeviceTypes'

const showNewDeviceTypeForm = ref(false);

const deviceTypes = inject<Ref<DeviceType[]>>("deviceTypes", ref([]));
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>('updateDeviceTypes', () => {});
const newDeviceTypeName = ref('');
const newDeviceTypeConnection = ref('');

const addNewDeviceType = () => {
  if (!newDeviceTypeName.value || !newDeviceTypeConnection.value) {
    if (!newDeviceTypeName.value) {
      console.error('Device type name is required');
    }
    if (!newDeviceTypeConnection.value) {
      console.error('Device type connection is required');
    }
  }

  const newDeviceType: DeviceType = {
    name: newDeviceTypeName.value,
    connectionType: newDeviceTypeConnection.value,
  };

  updateDeviceTypes([...deviceTypes.value, newDeviceType]);

  showNewDeviceTypeForm.value = false;
  newDeviceTypeName.value = '';
  newDeviceTypeConnection.value = '';
  showNewDeviceTypeForm.value = false;
};
</script>

<template>
  <main>
    <section class="flex justify-between">
      <form action="" class="w-2/3 flex gap-4">
        <BaseInputField />
        <BaseButton type="submit" class="mr-4">Search Devices</BaseButton>
      </form>
      <BaseButton class="w-fit mr-4" @click="showNewDeviceTypeForm = true">New device type</BaseButton>
    </section>
    <ul class="mr-4 grid grid-cols-1 gap-4">
      <DevicesCard 
        v-for="deviceType in deviceTypes" 
        :key="deviceType.name" 
        :deviceType="deviceType"
      />
    </ul>
    <form 
    class="absolute top-[50%] left-[50%] transform translate-x-[-50%] translate-y-[-50%] z-10
    w-96 
    bg-white-100 rounded-xl flex flex-col gap-6 p-4 shadow-md" 
    v-if="showNewDeviceTypeForm">
      <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold">Create New Device Type</h2>
        <BaseButton @click="showNewDeviceTypeForm = false">
          X
        </BaseButton>
      </div>
      <div className="flex flex-col gap-1">
        <label for="name" class="text-md">Name</label>
        <BaseInputField v-model="newDeviceTypeName" label="Name" name="name" />
        <p>Typed text: {{ newDeviceTypeName }}</p>
        <label for="connection-type" class="text-md">Connection type</label>
        <select name="connection-type" class="border border-accent-600 bg-primary-200 rounded-lg p-2" v-model="newDeviceTypeConnection">
          <option v-for="deviceType in deviceTypes" :key="deviceType.name" :value="deviceType.connectionType">{{ deviceType.connectionType }}</option>
        </select>
      </div>
      <div className="w-full flex justify-between">
        <BaseButton variant="outline" @click="showNewDeviceTypeForm = false">Cancel</BaseButton>
        <BaseButton type="submit" @click.prevent="addNewDeviceType">Create</BaseButton>
      </div>
    </form>
    <div v-if="showNewDeviceTypeForm" class="fixed inset-0 bg-[#000000] opacity-30"></div>
  </main>
</template>
