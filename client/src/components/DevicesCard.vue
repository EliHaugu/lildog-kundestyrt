<script setup lang="ts">
import { ref } from 'vue';
import BaseButton from '../components/BaseButton.vue';
import '@mdi/font/css/materialdesignicons.css';

// Import or define the DeviceType type
import type { DeviceType } from '../types/DeviceTypes';

defineProps({
  deviceType: {
    type: Object as () => DeviceType,
    required: true,
  },
});

const showDevices = ref(false);

const toggleDevices = () => {
  showDevices.value = !showDevices.value;
};
</script>

<template>
  <div class="p-2 h-fit min-w-96 rounded-xl border-2 border-[#dcdcdc] flex flex-col gap-2">
    <div
      :class="['flex justify-between items-center']"
    >
      <h2 class="px-2 text-xl font-semibold">{{ deviceType.name }}</h2>
      <div class="flex gap-2">
        <BaseButton class="w-fit">
            Add Device
            <i class="mdi mdi-plus text-xl p-1"></i>
        </BaseButton>
        <BaseButton class="w-fit bg-opacity-0 shadow-none" variant="secondary" @click="toggleDevices">
            <i v-if="showDevices" class="mdi mdi-chevron-up text-xl p-1"></i>
            <i v-else class="mdi mdi-chevron-down text-xl p-1"></i>
        </BaseButton>
      </div>
    </div>
    <div :class="['pt-2 w-full flex flex-row gap-2', showDevices ? 'border-t-2 border-[#d4d4d4]' : '']" v-if="showDevices">
      <ul class="w-full">
        <li 
          v-for="device in deviceType.devices" 
          :key="device.id"
          class="p-2 w-full rounded-md hover:bg-[#e3e3e3] hover:cursor-pointer flex flex-row"
        >
          <div class="w-full">
            {{ device.name }}
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
