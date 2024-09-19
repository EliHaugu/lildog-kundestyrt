<script setup lang="ts">
import { ref } from 'vue'
import { listItems } from '@/assets/mock_data'

const response = ref([
  {
    id: 1,
    number: 300,
    status: 'OK'
  }
])

const testConnection = ref(false)
</script>

<template>
  <main class="flex h-[calc(100vh-4rem)] items-center justify-center bg-white-100">
    <div class="w-1/2 rounded-xl p-6 shadow-xl">
      <h2 class="text-lg text-accent-700">Add new device</h2>
      <form action="" class="relative flex flex-col gap-2 pb-6 pt-4">
        <label for="newDeviceName">Name Device:</label>
        <input
          type="text"
          placeholder="Device name"
          class="rounded-lg border border-accent-600 px-4 py-2"
        />
        <div>
          <label for="newConnectionType">Connection Type:</label>
          <select
            name="newConnectionType"
            id=""
            class="ml-4 mt-2 rounded bg-accent-600 text-white-100"
          >
            <option value="ble">BLE</option>
            <option value="lte">LTE</option>
            <option value="wifi">WiFi</option>
            <option value="ade">ADE</option>
          </select>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <button
            type="button"
            v-on:click="testConnection = !testConnection"
            class="rounded-xl bg-accent-600 px-4 py-2 text-white-100 shadow-md hover:bg-accent-500"
          >
            Test Connection
          </button>
          <label>Response:</label>
          <label class="font-bold" v-if="testConnection" for="response"
            >{{ response[0].number }} {{ response[0].status }}</label
          >
        </div>
        <hr class="divider mt-4" />
        <div class="mt-4 flex flex-col gap-2 sm:flex-row">
          <select name="Add to board" id="" class="text-bg-900 rounded-xl bg-accent-500 pl-2">
            <option value="" disabled selected>Select Board</option>
            <option v-for="item in listItems" :key="item.id">
              {{ item.name }}
            </option>
          </select>
          <button
            type="submit"
            class="text-bg-900 rounded-xl bg-accent-400 px-4 py-2 shadow-md hover:bg-accent-500"
          >
            Add to devices
          </button>
          <button
            type="button"
            class="text-bg-700 rounded-xl bg-white-100 px-4 py-2 shadow-md hover:bg-accent-500"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </main>
</template>
