<script setup lang="ts">
import { ref } from 'vue';
import BaseButton from '../components/BaseButton.vue';

defineProps({
  deviceType: String,
  devices: Object
});

const showDevices = ref(true);

const toggleDevices = () => {
  showDevices.value = !showDevices.value;
};
</script>

<template>
  <div class="p-2 h-fit min-w-96 rounded-xl border-2 border-[#dcdcdc] shadow-md flex flex-col gap-2">
    <div
      :class="['flex justify-between items-center']"
    >
      <h2 class="px-2 text-xl font-semibold">{{ deviceType }}</h2>
      <div class="flex gap-2">
        <BaseButton class="w-fit">Add device</BaseButton>
        <BaseButton class="w-fit" @click="toggleDevices">
          {{ showDevices ? 'Hide' : 'Show' }} devices
        </BaseButton>
      </div>
    </div>
    <div :class="['pt-2 w-full flex flex-row gap-2', showDevices ? 'border-t-2 border-[#d4d4d4]' : '']" v-if="showDevices">
      <ul class="w-full">
        <li 
          v-for="device in devices" 
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
