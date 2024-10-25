<script setup lang="ts">
import BaseButton from '@/components/BaseButton.vue'
import BaseInputField from './BaseInputField.vue'
import type { Flow } from '@/types/FlowType'
import EditPen from '@/icons/EditPen.vue'
import { router } from '@/router'
import PlayIcon from '@/icons/RightArrow.vue'
import { inject, ref, type Ref } from 'vue'

const props = defineProps<{
  flow: Flow
}>()

const flows = inject<Ref<Flow[]>>('flows', ref([]))

const navigateToFlow = (id: string) => {
  const currentPath = router.currentRoute.value.fullPath
  router.push(`${currentPath}/${id}`)
}

// Flow editor
const showEditFlowForm = ref(false)

const editFlowType = ref<Flow | null>(null)

const editFlow = (flow: Flow) => {
  editFlowType.value = { ...flow }
  showEditFlowForm.value = true
}

const cancelEditFlow = () => {
  editFlowType.value = null
  showEditFlowForm.value = false
}

const updateFlow = () => {
  if (!editFlowType.value) return

  const updatedFlowTypes = flows.value.map((flow) => {
    if (flow.id === props.flow.id && editFlowType.value) {
      return { ...editFlowType.value }
    }
    return flow
  })

  updateFlowCard(updatedFlowTypes)
  editFlowType.value = null
  showEditFlowForm.value = false
}

const updateFlowCard = inject<(newFlowTypes: Flow[]) => void>('updateFlows', () => {
  console.error('updateFlows function not provided')
})
</script>

<template>
  <div
    class="h-40 w-[25rem] cursor-pointer rounded-md bg-secondary-50 p-3 hover:shadow-md dark:bg-accent-700"
    @click="navigateToFlow(flow.id)"
    style="z-index: 1"
  >
    <div :class="['flex items-center justify-between']">
      <h2 class="text-lg font-semibold">{{ flow.name }}</h2>
      <base-button
        @click.stop="editFlow(flow)"
        variant="outline"
        class="h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <edit-pen />
      </base-button>
    </div>
    <div class="mt-1 flex gap-1">
      <label
        class="my-2 mr-6 flex cursor-pointer content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-success': flow.status === 'Completed',
          'bg-warning': flow.status === 'In-progress',
          'bg-error': flow.status === 'Failed',
          'bg-accent-500': flow.status === 'Untested'
        }"
      >
        {{ flow.status }}
      </label>
      <label
        v-for="(connectionType, index) in flow.connectionTypes"
        :key="index"
        class="my-2 flex cursor-pointer content-start items-center justify-center rounded-xl px-2 text-white-100"
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
      @click.stop=""
    >
      Run Flow <play-icon fill="white" />
    </base-button>
  </div>
  <!-- flow editor -->
  <form
    class="absolute left-[50%] top-[50%] z-10 flex w-96 translate-x-[-50%] translate-y-[-50%] transform flex-col gap-6 rounded-xl bg-white-100 p-4 pt-6 shadow-md"
    v-if="showEditFlowForm && editFlowType"
  >
    <h2 class="text-lg font-semibold">Edit - Flow</h2>
    <div class="flex flex-col gap-1">
      <label for="name" class="text-md">Device flow name</label>
      <base-input-field v-model="editFlowType.name" label="Name" name="name" placeholder="" />
    </div>
    <div class="mt-6 flex justify-between gap-6">
      <base-button variant="outline" @click="cancelEditFlow">Cancel</base-button>
      <base-button @click="updateFlow">Update</base-button>
    </div>
  </form>
  <div
    v-if="showEditFlowForm"
    class="fixed inset-0 bg-[#000000] opacity-30"
    style="z-index: 2"
  ></div>
</template>
