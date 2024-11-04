<script setup lang="ts">
import type { BaseNode as Node } from '@/types/NodeType'
import { updateNode, deleteNode as removeNode } from '@/services/NodesService'
import useDragAndDrop from '@/composables/useDragAndDrop'
import { ref } from 'vue'

import BaseInputField from '../common/BaseInputField.vue'
import BaseModal from '../common/BaseModal.vue'
import BaseButton from '../common/BaseButton.vue'

import DeleteIcon from '@/icons/DeleteIcon.vue'
import EditPen from '@/icons/EditPen.vue'

const emit = defineEmits(['update'])
const props = defineProps({
  node: {
    type: Object as () => Node,
    required: true
  }
})

const editNodeModel = ref({
  label: props.node.data.label,
  node_type: props.node.data.node_type,
  device: props.node.data.device.toString(),
  function: props.node.data.function
})

const { onDragStart } = useDragAndDrop()

const editNode = () => {
  const node = {
    label: editNodeModel.value.label,
    node_type: editNodeModel.value.node_type,
    device: Number(editNodeModel.value.device),
    function: editNodeModel.value.function
  }
  updateNode(parseInt(props.node.id), node).then(() => {
    emit('update')
  })
}

const deleteNode = () => {
  removeNode(parseInt(props.node.id)).then(() => {
    emit('update')
  })
}

const openModal = () => {
  ;(document.getElementById('editNode') as HTMLDialogElement).showModal()
}
</script>

<template>
  <li
    :draggable="true"
    @dragstart="onDragStart($event, node)"
    class="mx-1 flex h-9 items-center gap-1 rounded-lg bg-primary-200 py-1.5 pl-4 shadow-md hover:cursor-grab"
  >
    <p>{{ node.data.label }}</p>
    <base-button @click="openModal" variant="icon" class="ml-auto h-7 items-center">
      <edit-pen class="fill-accent-900 dark:fill-white-100" />
    </base-button>
    <base-button @click="deleteNode" variant="icon" class="mr-1 h-7 items-center">
      <delete-icon class="fill-error" />
    </base-button>

    <base-modal id="editNode" submitButtonText="Change" title="Edit Node" @submit="editNode">
      <base-input-field v-model="editNodeModel.label" label="Label" name="label" placeholder="" />
      <base-input-field
        v-model="editNodeModel.node_type"
        label="Node type"
        name="node-type"
        placeholder=""
        type="select"
        :options="['Assert', 'Action']"
      />
      <base-input-field
        v-model="editNodeModel.device"
        label="Device"
        name="device"
        placeholder=""
        type="number"
      />
      <base-input-field
        v-model="editNodeModel.function"
        type="textarea"
        label="Function"
        name="Function"
        placeholder=""
      />
    </base-modal>
  </li>
</template>
