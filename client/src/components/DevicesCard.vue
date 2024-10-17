<script setup lang="ts">
import { ref } from 'vue'
import BaseInputField from './BaseInputField.vue'
import BaseButton from './BaseButton.vue'

defineProps({
  device: Object
})

const showSaveButton = ref(false)
</script>

<template>
  <li class="z-10 h-full min-w-96 rounded-xl bg-primary-100 p-4 shadow-md">
    <div class="flex">
      <h2 class="text-lg">{{ device!.name }}</h2>
      <h3 v-if="showSaveButton" class="ml-auto text-accent-800/50">Unsaved</h3>
    </div>
    <form
      v-on:change="showSaveButton = !showSaveButton"
      action=""
      class="relative flex flex-col gap-2 pb-14 pt-4"
    >
      <label for="deviceName">Name Device:</label>
      <BaseInputField :placeholder="device!.name" />
      <div class="flex items-center">
        <label for="connectionType">Connection Type:</label>
        <select
          name="connectionType"
          id=""
          :value="device!.type"
          class="ml-4 mt-2 bg-accent-600 text-white-100"
        >
          <option value="ble">BLE</option>
          <option value="lte">LTE</option>
          <option value="wifi">WiFi</option>
          <option value="ade">ADE</option>
        </select>
        <BaseButton v-if="showSaveButton" class="ml-auto"> Save Changes </BaseButton>
      </div>
    </form>
  </li>
</template>
