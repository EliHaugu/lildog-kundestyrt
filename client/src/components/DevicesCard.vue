<script setup lang="ts">
import { ref } from 'vue'

defineProps({
  device: Object
})

const showSaveButton = ref(false)
</script>

<template>
  <li class="h-full min-w-96 rounded-xl bg-white-100 p-4 text-accent-600 shadow-md">
    <div class="flex">
      <h2 class="text-lg text-accent-700">{{ device!.name }}</h2>
      <h3 v-if="showSaveButton" class="ml-auto text-accent-800/50">Unsaved</h3>
    </div>
    <form
      v-on:change="showSaveButton = !showSaveButton"
      action=""
      class="relative flex flex-col gap-2 pb-14 pt-4"
    >
      <label for="deviceName">Name Device:</label>
      <input
        type="text"
        :placeholder="device!.name"
        class="rounded-lg border border-accent-600 px-4 py-2"
      />
      <div>
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
      </div>

      <button
        v-if="showSaveButton"
        class="absolute bottom-0 right-0 rounded-xl bg-accent-600 px-4 py-2 text-white-100 shadow-md hover:bg-accent-500"
      >
        Save Changes
      </button>
    </form>
  </li>
</template>
