<script setup lang="ts">
import DevicesCard from '@/components/DevicesCard.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInputField from '@/components/BaseInputField.vue'

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
        <BaseInputField />
        <BaseButton type="submit" class="mb-4 mr-4"> Search Devices </BaseButton>
      </form>
    </section>
    <ul class="mr-4 grid gap-4 xl:grid-cols-2">
      <devices-card v-for="device in devices" :key="device.id" :device="device" />
    </ul>
  </main>
</template>
