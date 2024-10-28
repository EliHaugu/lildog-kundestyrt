<script setup lang="ts">
import { ref, provide } from 'vue'
import Layout from '@/components/PageLayout.vue'
import { mock_device_types, mock_flows } from '@/assets/mock_data'
import type { DeviceType } from '@/types/DeviceTypes'
import type { Flow } from './types/FlowType'

const deviceTypes = ref<DeviceType[]>(mock_device_types)

function updateDeviceTypes(newData: DeviceType[]) {
  deviceTypes.value = newData
}

provide('deviceTypes', deviceTypes)
provide('updateDeviceTypes', updateDeviceTypes)

const flows = ref<Flow[]>(mock_flows)

function updateFlows(newData: Flow[]) {
  flows.value = newData
}

provide('flows', flows)
provide('updateFlows', updateFlows)
</script>
<template>
  <Layout>
    <RouterView class="flex-grow z-10 my-5 mr-5 p-8 bg-accent-900 rounded-3xl" />
  </Layout>
</template>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/minimap/dist/style.css';
</style>
