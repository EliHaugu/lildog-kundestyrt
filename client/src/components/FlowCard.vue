<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInputField from './common/BaseInputField.vue'
import Modal from './common/Modal.vue'
import type { Flow } from '@/types/FlowType'
import EditPen from '@/icons/EditPen.vue'
import DeleteIcon from '@/icons/DeleteIcon.vue'
import PlayIcon from '@/icons/RightArrow.vue'
import { ref, defineEmits, inject, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import flowService from '@/services/FlowService'

defineProps<{
  flow: Flow
  connectionTypes: string[]
}>()
const emit = defineEmits(['flowUpdated'])

const router = useRouter()
const showEditFlowForm = ref(false)
const editFlowType = ref<Flow | null>(null)
const flows = inject<Ref<Flow[]>>('flows', ref([]))

const navigateToFlow = (id: string) => {
  const currentPath = router.currentRoute.value.fullPath
  router.push(`${currentPath}/${id}`)
}

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

const cancelEditFlow = () => {
  editFlowType.value = null
  showEditFlowForm.value = false
}


const editFlow = (flow: Flow) => {
  editFlowType.value = { ...flow }
  ;(document.getElementById(`editFlowForm${flow.id}`) as HTMLDialogElement).showModal()
}

const updateFlow = async () => {
  if (!editFlowType.value) return

  try {
    await flowService.updateFlow(editFlowType.value.id, editFlowType.value)
    console.log('Flow updated')
    emit('flowUpdated')
    showEditFlowForm.value = false
  } catch (error) {
    console.error('Error updating flow:', error)
  } finally {
    editFlowType.value = null
  }
}
</script>

<template>
  <div
    class="h-40 w-[25rem] cursor-pointer rounded-md bg-secondary-50 p-3 hover:shadow-md dark:bg-accent-700"
    @click="navigateToFlow(flow.id)"
    style="z-index: 1"
  >
    <div :class="['flex items-center']">
      <h2 class="text-lg font-semibold">{{ flow.name }}</h2>
      <base-button
        @click.stop="deleteFlow(flow.id)"
        variant="outline"
        class="ml-auto h-fit rounded-lg border-none bg-secondary-50 shadow-none dark:bg-accent-700"
      >
        <delete-icon fill="red" />
      </base-button>
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
        v-for="(connectionType, index) in flow.combinedData"
        :key="index"
        class="my-2 flex cursor-pointer content-start items-center justify-center rounded-xl px-2 text-white-100"
        :class="{
          'bg-ble': connectionType === 'uart',
          'bg-wifi': connectionType === 'wifi',
          'bg-ade': connectionType === 'adb'
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

  <base-modal
    :id="'editFlowForm' + flow.id"
    submitButtonText="Update"
    title="Edit Flow"
    @submit="updateFlow"
  >
    <base-input-field label="Name" name="name" placeholder="" />
  </base-modal>
</template>
