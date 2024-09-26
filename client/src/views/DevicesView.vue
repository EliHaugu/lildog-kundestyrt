<script setup lang="ts">
import DevicesCard from '@/components/DevicesCard.vue'

const devices = [
  {
    id: 1,
    name: 'Device 1',
    type: 'ble',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 2,
    name: 'Device 2',
    type: 'ade',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  },
  {
    id: 3,
    name: 'Device 3',
    type: 'wifi',
    connection: 'X43476342',
    fields: {
      key: 'zxvc_234523',
      value: '1234'
    }
  }
]
</script>

<template>
  <main>
    <section>
      <form action="" class="flex gap-4">
        <input
          type="text"
          placeholder="Search..."
          class="mb-4 w-auto flex-grow rounded-xl border border-accent-500 bg-primary-100 px-4 py-2"
        />
        <button
          type="submit"
          class="mb-4 ml-auto mr-4 rounded-xl bg-accent-600 px-4 text-white-100"
        >
          Search Devices
        </button>
      </form>
    </section>
    <ul class="mr-4 grid gap-4 xl:grid-cols-2">
      <devices-card v-for="device in devices" :key="device.id" :device="device" />
    </ul>
  </main>
</template>
