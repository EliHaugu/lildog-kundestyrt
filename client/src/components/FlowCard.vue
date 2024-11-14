<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInputField from './common/BaseInputField.vue'
import type { Flow } from '@/types/FlowType'
import EditPen from '@/icons/EditPen.vue'
import PlayIcon from '@/icons/PlayIcon.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'
import { ref, defineEmits, computed } from 'vue'
import flowService from '@/services/FlowService'
import BaseModal from './common/BaseModal.vue'
import { runTest } from '@/services/TestService'

const emit = defineEmits(['flowUpdated'])
const props = defineProps<{
  flow: Flow
  connectionTypes?: string[]
  communicationProtocols?: string[]
}>()

const editFlowType = ref<Flow | null>(null)
const flow = ref<Flow>(props.flow)

const editFlowName = computed({
  get: () => editFlowType.value?.name || '',
  set: (newName: string) => {
    if (editFlowType.value) {
      editFlowType.value.name = newName
    }
  }
})

const deleteFlow = async (id: string) => {
  const userConfirmed = confirm('Are you sure you want to delete this flow?')

  if (userConfirmed) {
    try {
      await flowService.deleteFlow(id)
      console.log('Flow deleted successfully')
      emit('flowUpdated')
    } catch (error) {
      console.error('Error deleting flow:', error)
    }
  } else {
    console.log('User canceled the deletion')
  }
}

const editFlow = (flow: Flow) => {
  editFlowType.value = { ...flow }
  ;(document.getElementById(`editFlowForm${flow.id}`) as HTMLDialogElement).showModal()
}

const updateFlow = async () => {
  if (!editFlowType.value) return

  try {
    await flowService.updateFlow(editFlowType.value.id, editFlowType.value)
    emit('flowUpdated')
  } catch (error) {
    console.error('Error updating flow:', error)
  } finally {
    editFlowType.value = null
  }
}

const test = (flowId: string) => {
  runTest(flowId)
    .then((response) => {
      flow.value.status = response.results[0].status
    })
    .catch((error) => {
      console.error('Error running test:', error)
    })
}
</script>

<template>
  <router-link
    class="relative h-40 cursor-pointer rounded-md bg-secondary-50 p-3 transition-all duration-200 hover:bg-opacity-50 hover:shadow-md dark:bg-accent-700"
    :to="'flow/' + flow.id"
  >
    <div class="flex items-center gap-2">
      <h2 class="text-lg font-semibold">{{ flow.name }}</h2>
      <base-button
        @click.stop="editFlow(flow)"
        aria-label="Edit flow"
        variant="outline"
        class="icon ml-auto bg-secondary-50 dark:bg-accent-700"
      >
        <edit-pen />
      </base-button>
      <base-button
        @click.stop="deleteFlow(flow.id)"
        variant="outline"
        aria-label="Delete flow"
        class="icon bg-secondary-50 dark:bg-accent-700"
      >
        <delete-icon />
      </base-button>
    </div>

    <div class="mt-1 flex gap-1">
      <div
        class="my-2 mr-6 flex cursor-pointer content-start items-center justify-center rounded-xl bg-accent-500 px-2 text-white-100"
        :class="{
          'bg-success': flow.status === 'success',
          'bg-warning': flow.status === 'warning',
          'bg-error': flow.status === 'failed'
        }"
      >
        <p v-if="flow.status">{{ flow.status }}</p>
        <p v-else>Idle</p>
      </div>
      <div
        v-for="(connectionType, index) in flow.connectionType"
        :key="index"
        class="my-2 flex cursor-pointer content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-success': connectionType === 'uart',
          'bg-adb': connectionType === 'adb'
        }"
      >
        {{ connectionType }}
      </div>
      <div
        v-for="(communicationProtocol, index) in flow.communicationProtocol"
        :key="index"
        class="my-2 flex cursor-pointer content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-wifi': communicationProtocol === 'wifi',
          'bg-ble': communicationProtocol === 'bluetooth',
          'bg-lte': communicationProtocol === 'lte'
        }"
      >
        {{ communicationProtocol }}
      </div>
    </div>
    <base-button
      variant="light"
      class="absolute bottom-4 right-4 flex h-6 items-center gap-2 rounded-xl border-0 text-white-100"
      @click.stop="test(flow.id)"
    >
      Run Flow <play-icon fill="white" />
    </base-button>
  </router-link>

  <base-modal
    :id="'editFlowForm' + flow.id"
    submitButtonText="Update"
    title="Edit Flow"
    @submit="updateFlow"
  >
    <base-input-field v-model="editFlowName" label="Name" name="name" placeholder="" />
  </base-modal>
</template>
