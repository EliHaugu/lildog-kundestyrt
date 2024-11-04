<script setup lang="ts">
import type { Device, DeviceModel, DeviceCategory } from '@/types/DeviceTypes';
import { computed, inject, onMounted, ref, type Ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { createDevice, fetchDevicesByCategory } from '@/services/DevicesService';
import { deleteCategory } from '@/services/CategoryService';

import DeviceInstance from '@/components/devices/DeviceInstance.vue';
import BaseButton from '@/components/common/BaseButton.vue';
import DeviceModal from '@/components/devices/DeviceModal.vue';

import PlusIcon from '@/icons/PlusIcon.vue';
import ChevronRightIcon from '@/icons/ChevronRightIcon.vue';

const devices = ref<Device[]>([]);
const router = useRouter();
const route = useRoute();

const deviceCategories = inject<Ref<DeviceCategory[]>>('deviceCategories', ref([]));
const categoryId: number = parseInt(route.params.id as string);
console.log('categoryId', categoryId);
console.log('deviceCategories', deviceCategories.value);

const deviceCategory = computed(() => {
  return deviceCategories.value.find((category) => category.id === categoryId);
});

onMounted(async () => {
  devices.value = await fetchDevicesByCategory(deviceCategory.value?.name || '');
});

const openModal = () => {
  (document.getElementById('newDeviceModal') as HTMLDialogElement).showModal();
};

const newDevice = async (newDeviceModel: DeviceModel) => {
  const device = {
    id: devices.value.length + 1,
    device_id: newDeviceModel.device_id,
    category: deviceCategory.value?.id || 0,
    connection_ids: {
      adb_device_id: newDeviceModel.connection_ids.adb_device_id,
      serial_number: newDeviceModel.connection_ids.serial_number,
    },
    communication_ids: {
      mac_address: newDeviceModel.communication_ids.mac_address,
    },
  };

  const res = await createDevice(device);
  if (res) {
    update();
  } else {
    console.error('Failed to create device');
  }
};

const update = async () => {
  devices.value = await fetchDevicesByCategory(deviceCategory.value?.name || '');
};

const deleteCategoryFunc = async () => {
  if (!deviceCategory.value) return;
  const confirmed = confirm(`Are you sure you want to delete ${deviceCategory.value.name}?`);
  if (confirmed) {
    const success = await deleteCategory(deviceCategory.value.id);
    if (success) {
      router.push('/categories');
    } else {
      console.error('Failed to delete device category');
    }
  }
};
</script>

<template>
  <main class="pb-8 pr-4">
    <div class="flex h-full flex-col gap-2">
      <div class="flex grow-0 items-center gap-2">
        <router-link
          to="/categories"
          class="rounded-md px-2 py-1 text-xl font-semibold hover:bg-accent-800 hover:text-white-100"
          >Device categories</router-link
        >
        <chevron-right-icon />
        <h1 class="text-xl font-semibold">{{ deviceCategory?.name }}</h1>
      </div>

      <!-- Delete Category Button -->
      <base-button
        variant="outline"
        class="mt-3 w-fit bg-red-500 text-white"
        @click="deleteCategoryFunc"
      >
        Delete Category
      </base-button>

      <div class="z-20 flex grow-0 justify-start gap-6">
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Connection types:</p>
          <div class="my-2 flex flex-wrap">
            <label
              v-for="connectionType in deviceCategory?.connectionTypes || []"
              :key="connectionType"
              class="mx-1 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
              :class="{
                'bg-blue-500': connectionType === 'adb',
                'bg-green-500': connectionType === 'uart'
              }"
            >
              {{ connectionType }}
            </label>
          </div>
        </div>
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Communication protocols:</p>
          <div class="my-2 flex flex-wrap">
            <label
              v-for="protocol in deviceCategory?.communicationProtocols || []"
              :key="protocol"
              class="mx-1 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
              :class="{
                'bg-purple-500': protocol === 'wifi',
                'bg-red-500': protocol === 'bluetooth',
                'bg-yellow-500': protocol === 'lte'
              }"
            >
              {{ protocol }}
            </label>
          </div>
        </div>
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Number of devices:</p>
          <p
            class="m-2 w-fit rounded-xl border-2 border-[#6B8AFA] bg-accent-600 px-2 text-white-100"
          >
            {{ devices?.length === 1 ? '1 device' : `${devices?.length || 0} devices` }}
          </p>
        </div>
      </div>
      <div class="flex grow flex-col gap-2 overflow-y-auto">
        <div class="flex grow-0 items-center justify-between gap-6">
          <div class="z-20 flex w-full items-center justify-start gap-3 text-xl font-semibold">
            <h2 class="w-12">ID</h2>
            <h2 class="w-64">Device instance name</h2>
            <h2 class="w-12">Status</h2>
          </div>
          <base-button class="justify-between text-nowrap rounded-md" @click="openModal">
            Add device <plus-icon />
          </base-button>
        </div>
        <div class="flex grow flex-col gap-2 overflow-y-auto">
          <device-instance
            @update="update"
            v-for="device in devices"
            :key="device.id"
            :device="device"
          />
        </div>
      </div>
    </div>
    <device-modal id="newDeviceModal" submit="Create" title="New Device" @submit="newDevice" />
  </main>
</template>
