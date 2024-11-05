<script setup lang="ts">
import { ref, provide } from 'vue'
import Layout from '@/components/PageLayout.vue'
import { mock_device_types, mock_flows } from '@/assets/mock_data'
import type { DeviceCategory } from '@/types/DeviceTypes'
import type { Flow } from './types/FlowType'

const deviceCategories = ref<DeviceCategory[]>(mock_device_types)

provide('deviceCategories', deviceCategories)

const flows = ref<Flow[]>(mock_flows)

function updateFlows(newData: Flow[]) {
  flows.value = newData
}

provide('flows', flows)
provide('updateFlows', updateFlows)
</script>
<template>
  <Layout>
    <RouterView class="z-10 my-2 mr-2 flex-grow rounded-2xl bg-white-200 p-4 dark:bg-accent-900" />
  </Layout>
</template>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/minimap/dist/style.css';
</style>
