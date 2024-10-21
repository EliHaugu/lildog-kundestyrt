<script setup lang="ts">
import BaseButton from '@/components/BaseButton.vue'
import type { Flow, Flows } from '@/types/FlowType'
import { inject, type Ref, ref } from 'vue'
import EditPen from '@/icons/EditPen.vue'
import { router } from '@/router'
import RightArrow from '@/icons/RightArrow.vue'

const flows = inject<Ref<Flows>>('flows', ref([]))
const props = defineProps<{
  flow: Flow
}>()

const navigateToFlow = (id: string) => {
  const currentPath = router.currentRoute.value.fullPath
  router.push(`${currentPath}/${props.flow.id}`)
}
</script>

<template>
  <div class="h-40 w-[25rem] rounded-md bg-secondary-50 p-3 dark:bg-accent-700" style="z-index: 1">
    <div :class="['flex items-center justify-between']">
      <h2 class="text-lg font-semibold">{{ flow.name }}</h2>
      <base-button
        variant="outline"
        class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <edit-pen />
      </base-button>
    </div>
    <div class="mt-1 flex gap-1">
      <label
        class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-success': flow.status === 'Completed',
          'bg-warning': flow.status === 'In-progress',
          'bg-error': flow.status === 'Inactive'
        }"
      >
        {{ flow.status }}
      </label>
      <label
        v-for="(connectionType, index) in flow.connectionTypes"
        :key="index"
        class="my-2 flex content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-ble': connectionType === 'BLE',
          'bg-wifi': connectionType === 'WiFi',
          'bg-ade': connectionType === 'ADE'
        }"
      >
        {{ connectionType }}
      </label>
    </div>
    <base-button
      variant="light"
      class="ml-auto mt-7 flex h-6 items-center gap-2 rounded-xl border-0 text-white-100"
      @click="navigateToFlow(flow.id)"
    >
      Run Flow <right-arrow fill="white" />
    </base-button>
  </div>
</template>
