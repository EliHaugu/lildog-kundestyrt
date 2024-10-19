<script setup lang="ts">
import { defineEmits, ref } from 'vue';
import type { Device } from '@/types/DeviceTypes';
import CheckIcon from '@/icons/CheckIcon.vue';
import EditPen from '@/icons/EditPen.vue';
import DeleteIcon from '@/icons/DeleteIcon.vue';

const props = defineProps<{
    device: Device;
}>();

const device = ref(props.device);

const emit = defineEmits(['edit-device', 'delete-device']);

const editDevice = () => {
    emit('edit-device', device);
};

const deleteDevice = () => {
    emit('delete-device', device);
};
</script>

<template>
    <div class="px-2 py-1 rounded-md hover:bg-secondary-50 flex justify-between items-center gap-6">
        <div class="flex justify-start items-center gap-3">
            <p class="w-12">{{ device.id }}</p>
            <p class="w-64">{{ device.name }}</p>
            <div class="w-fit p-1 rounded-full bg-success">
                <check-icon />
            </div>
        </div>
        <div class="flex justify-start items-center gap-3">
            <button class="w-fit p-1 rounded-lg hover:bg-accent-500" @click="editDevice">
                <edit-pen />
            </button>
            <button class="w-fit p-1 rounded-lg hover:bg-accent-500 text-error" @click="deleteDevice">
                <delete-icon />
            </button>
        </div>
    </div>
</template>