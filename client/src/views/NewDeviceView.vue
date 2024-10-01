<template>
  <main class="flex h-[calc(100vh-4rem)] items-center justify-center bg-primary-200">
    <div class="w-1/2 rounded-xl bg-primary-100 p-6 shadow-xl">
      <h2 class="text-lg">Add new device</h2>
      <form action="" class="relative flex flex-col gap-2 pb-6 pt-4">
        <label for="newDeviceName">Name Device:</label>
        <BaseInputField placeholder="Device name" />
        <div>
          <label for="newConnectionType">Connection Type:</label>
          <select
            name="newConnectionType"
            id="newConnectionType"
            class="ml-4 mt-2 rounded bg-accent-600 text-white-100"
          >
            <option value="ble">BLE</option>
            <option value="lte">LTE</option>
            <option value="wifi">WiFi</option>
            <option value="ade">ADE</option>
          </select>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <BaseButton @click="toggleTestConnection"> Test Connection </BaseButton>

          <label>Response:</label>
          <label class="font-bold" v-if="testConnection" for="response">
            {{ response[0].number }} {{ response[0].status }}
          </label>
        </div>
        <hr class="divider mt-4" />
        <div class="mt-4 flex flex-col gap-2 sm:flex-row">
          <select name="Add to board" id="" class="text-bg-900 rounded-xl bg-accent-500 pl-2">
            <option value="" disabled selected>Select Board</option>
            <option v-for="item in listItems" :key="item.id">
              {{ item.name }}
            </option>
          </select>
          <BaseButton variant="secondary" type="submit"> Add to devices </BaseButton>
          <BaseButton variant="outline" @click="cancelAction"> Cancel </BaseButton>
        </div>
      </form>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import { listItems } from '@/assets/mock_data'

const response = ref([
  {
    id: 1,
    number: 300,
    status: 'OK',
    name: 'Device 1'
  }
])

const testConnection = ref(false)

const toggleTestConnection = () => {
  testConnection.value = !testConnection.value
}

const cancelAction = () => {
  // Handle cancel action here
}
</script>
