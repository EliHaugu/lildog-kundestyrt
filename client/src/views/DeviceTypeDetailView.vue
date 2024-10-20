<script setup lang="ts">
import type { DeviceType, Device } from '@/types/DeviceTypes'
import { computed, inject, ref, type Ref } from 'vue';
import { useRoute } from 'vue-router';
import BaseButton from '@/components/BaseButton.vue';
import BaseInputField from '@/components/BaseInputField.vue';
import DeviceInstance from '@/components/devices/DeviceInstance.vue';
import PlusIcon from '@/icons/PlusIcon.vue';

const route = useRoute()
const deviceTypeName = computed(() => route.params.deviceTypeName as string)
const deviceTypes = inject<Ref<DeviceType[]>>('deviceTypes', ref([]))
const updateDeviceTypes = inject<(newDeviceTypes: DeviceType[]) => void>(
  'updateDeviceTypes',
  () => {}
)
const deviceType = deviceTypes.value.find((type) => type.name === deviceTypeName.value)

const addNewDevice = ref<boolean>(false)
const newDeviceName = ref<string>('')
const editDevice = ref<Device | null>(null)
const showEditDeviceForm = ref<boolean>(false)

function handleAddNewDevice() {
    let newDeviceId: number;
    do {
        newDeviceId = Math.floor(100 + Math.random() * 900);
    } while (deviceType?.devices?.some(device => device.id === newDeviceId));
    const newDevice: Device = {
        id: newDeviceId,
        name: newDeviceName.value,
        deviceType: deviceType?.name || '',
        connectionType: deviceType?.connectionType || 'BLE',
        connectionId: '',
        fields: {
            key: '',
            value: '',
        },
    }

    if (deviceType) {
        deviceType.devices?.push(newDevice)
    }

    addNewDevice.value = false
    newDeviceName.value = ''
    updateDeviceTypes(deviceTypes.value)
}

function handleEditDevice(device: Device) {
    editDevice.value = { ...device };
    showEditDeviceForm.value = true;
}

function handleDeleteDevice(device: Device) {
    const index = deviceType?.devices?.findIndex((d) => d.id === device.id);
    if (index !== undefined && index !== -1 && deviceType && deviceType.devices) {
        console.log('Delete device:', device);
        deviceType.devices.splice(index, 1);
        updateDeviceTypes(deviceTypes.value);
    }
}

const updateDevice = () => {
    if (!editDevice.value) return;

    const updatedDeviceType: DeviceType = {
        ...deviceType!,
        devices: deviceType?.devices?.map((device) => {
            if (device.id === editDevice.value?.id) {
                return { ...editDevice.value }
            }
            return device
        })
    }

    const updatedDeviceTypes: DeviceType[] = deviceTypes.value.map((deviceType) => {
        if (deviceType.name === updatedDeviceType.name) {
        return { ...updatedDeviceType }
        }
        return deviceType
    })
    updateDeviceTypes(updatedDeviceTypes)
    editDevice.value = null
    showEditDeviceForm.value = false
}

function handleCancelEdit() {
    editDevice.value = null;
    showEditDeviceForm.value = false;
}

function handleCancelNewDevice() {
    addNewDevice.value = false;
}

</script>

<template>
    <main class="pr-4 pb-8">
        <div class="flex flex-col gap-12" v-if="deviceType">
            <div class="w-fit flex justify-between items-center gap-1">
                <router-link to="/devices" class="px-2 py-1 rounded-md text-2xl font-semibold hover:bg-accent-300">Configure devices</router-link>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
                <h1 class="text-2xl font-semibold">{{ deviceType.name }}</h1>
            </div>
            <div class="flex justify-start gap-6">
                <div class="w-fit flex justify-between items-center gap-1">
                    <p class="text-lg font-semibold">Connection type:</p>
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
                </div>
                <div class="w-fit flex justify-between items-center gap-1">
                    <p class="text-lg font-semibold">Number of devices:</p>
                    <label class="m-2 w-fit rounded-xl border-2 border-[#6B8AFA] bg-[#E6EBFE] px-2">
                        {{
                        deviceType.devices?.length === 1
                            ? '1 device'
                            : `${deviceType.devices?.length || 0}  devices`
                        }}
                    </label>
                </div>
            </div>
            <div class="flex flex-col gap-3">
                <div class="flex justify-between items-center gap-6">
                    <div class="w-full text-xl font-semibold flex justify-start items-center gap-3">
                        <h2 class="w-12">ID</h2>
                        <h2 class="w-64">Device instance name</h2>
                        <h2 class="w-12">Status</h2>
                    </div>
                    <base-button 
                    class="w-40 justify-between"
                    @click="addNewDevice = true"
                    >
                        Add device <plus-icon />
                    </base-button>
                </div>
                <div class="flex flex-col gap-3">
                    <device-instance 
                        v-for="device in deviceType.devices" 
                        :key="device.id" 
                        :device="device" 
                        @edit-device="handleEditDevice(device)" 
                        @delete-device="handleDeleteDevice(device)"
                    />
                </div>
            </div>
        </div>
        <div v-if="showEditDeviceForm && editDevice" class="absolute top-0 right-0 w-screen h-screen bg-[#000000] opacity-50"></div>
        <div v-if="showEditDeviceForm && editDevice" class="absolute top-[50%] left-[50%] transform translate-x-[-50%] translate-y-[-50%] p-6 rounded-xl bg-primary-100 border-2 border-accent-700">
            <h2 class="text-xl font-semibold mb-4">Edit Device</h2>
            <form>
                <div class="mb-4 flex flex-col gap-1">
                    <label for="name" class="text-md">Device type name</label>
                    <base-input-field v-model="editDevice.name" label="Name" name="name" placeholder="" />
                </div>
                <div class="flex justify-between gap-4">
                    <base-button variant="outline" @click="handleCancelEdit">Cancel</base-button>
                    <base-button @click="updateDevice">Update</base-button>
                </div>
            </form>
        </div>
        <div v-if="addNewDevice" class="absolute top-0 right-0 w-screen h-screen bg-[#000000] opacity-50"></div>
        <div v-if="addNewDevice" class="absolute top-[50%] left-[50%] transform translate-x-[-50%] translate-y-[-50%] p-6 rounded-xl bg-primary-100 border-2 border-accent-700">
            <h2 class="text-xl font-semibold mb-4">Add New Device</h2>
            <form>
                <div class="mb-4">
                    <label for="deviceName" class="block text-sm font-medium text-gray-700">Device Name</label>
                    <input
                        type="text"
                        id="deviceName"
                        v-model="newDeviceName"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        required
                    />
                </div>
                <div class="flex justify-between gap-4">
                    <base-button type="button" variant="outline" @click="handleCancelNewDevice">Cancel</base-button>
                    <base-button type="button" @click="handleAddNewDevice">Add new device</base-button>
                </div>
            </form>
        </div>
    </main>
</template>