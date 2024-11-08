<script setup lang="ts">
import type { Device, DeviceModel, DeviceCategory } from '@/types/DeviceTypes'
import { onBeforeMount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { createDevice, fetchDevicesByCategory } from '@/services/DevicesService'
import { deleteCategory , getCategory} from '@/services/CategoryService'

import DeviceInstance from '@/components/devices/DeviceInstance.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import DeviceModal from '@/components/devices/DeviceModal.vue'

import PlusIcon from '@/icons/PlusIcon.vue'
import ChevronRightIcon from '@/icons/ChevronRightIcon.vue'

const category = ref<DeviceCategory>({
  id: 0,
  category_name: '',
  connection_types: [],
  communication_protocols: []
})
const devices = ref<Device[]>([])
const router = useRouter()
const route = useRoute()



onMounted(async () => {
  category.value = await getCategory(Number(route.params.id))
  devices.value = await fetchDevicesByCategory(Number(route.params.id))
})


const openModal = () => {
  (document.getElementById('newDeviceModal') as HTMLDialogElement).showModal()
}

const newDevice = async (newDeviceModel: DeviceModel) => {
  const device = {
    id: devices.value.length + 1,
    device_id: newDeviceModel.device_id,
    category: category.value.id,
    connection_ids: {
      adb_device_id: newDeviceModel.connection_ids.adb_device_id,
      serial_number: newDeviceModel.connection_ids.serial_number
    },
    communication_ids: {
      mac_address: newDeviceModel.communication_ids.mac_address
    }
  }

  const res = await createDevice(device)
  if (res) {
    update()
  } else {
    console.error('Failed to create device')
  }
}

const update = async () => {
  devices.value = await fetchDevicesByCategory(category.value.id)
}

const deleteCategoryFunc = async () => {
  const confirmed = confirm(`Are you sure you want to delete this category?`)
  if (confirmed) {
    const success = await deleteCategory(category.value.id)
    if (success) {
      router.push('/categories')
    } else {
      console.error('Failed to delete device category')
    }
  }
}
</script>

<template>
  <main class="pb-8 pr-4">
    <div class="flex h-full flex-col gap-2">
      <div class="flex items-center gap-2">
        <router-link
          to="/categories"
          class="rounded-md px-2 py-1 text-xl font-semibold hover:bg-accent-800 hover:text-white-100"
          >Device categories</router-link
        >
        <chevron-right-icon />
        <h1 class="text-xl font-semibold">{{category.category_name}}</h1>
        <base-button
        variant="outline"
        class="bg-red-500 ml-auto text-white w-fit"
        @click="deleteCategoryFunc"
      >
        Delete Category
      </base-button>
      </div>
      <div class="z-20 flex grow-0 justify-start gap-6">
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Connection types:</p>
          <div class="my-2 flex flex-wrap">
            <div
              v-for="connectionType in category.connection_types"
              :key="connectionType"
              class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
              :class="{
                'bg-ble': connectionType === 'uart',
                'bg-ade': connectionType === 'adb'
              }"
            >
              {{ connectionType }}
            </div>
          </div>
        </div>
        <div class="flex w-fit items-center justify-between gap-1">
          <p class="text-lg font-semibold">Communication protocols:</p>
          <div class="my-2 flex flex-wrap">
            <div
              v-for="protocol in category.communication_protocols"
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
