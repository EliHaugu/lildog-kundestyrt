<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import NodesListItem from './NodesListItem.vue'

import ChevronDownIcon from '@/icons/ChevronDownIcon.vue'
import ChevronUpIcon from '@/icons/ChevronUpIcon.vue'
import PlusIcon from '@/icons/PlusIcon.vue'

import type { BaseNode as Node } from '@/types/NodeType'
import { fetchNodes } from '@/services/NodesService'
import { onMounted, ref, watch } from 'vue'

import { createNode } from '@/services/NodesService'
import BaseModal from '../common/BaseModal.vue'

const storedNodesOpen = ref(false)

const newNodeModel = ref({
  label: '',
  node_type: '',
  device: '',
  function: ''
})
const selectedTab = ref(0)
const resNodes = ref<Node[]>()
const nodes = ref<Node[]>([])

const openModal = () => {
  ;(document.getElementById('newNode') as HTMLDialogElement).showModal()
}

watch(selectedTab, () => {
  filterNodes(selectedTab.value)
})

const filterNodes = (tab: number) => {
  nodes.value = resNodes.value!.filter(
    (node) => node.data.node_type === (tab === 0 ? 'Assert' : 'Action')
  )
}

const getNodes = async () => {
  fetchNodes()
    .then((data) => {
      resNodes.value = data
    })
    .finally(() => {
      filterNodes(selectedTab.value)
    })
}

onMounted(() => {
  getNodes()
})

const newNode = () => {
  const node = {
    label: newNodeModel.value.label,
    node_type: newNodeModel.value.node_type,
    device: Number(newNodeModel.value.device) || undefined,
    function: newNodeModel.value.function,
    x_pos: 0,
    y_pos: 0
  }
  createNode(node).then((res: Boolean) => {
    if (res) {
      // Would be better to add it to the list without a new fetch.
      getNodes()
    } else {
      console.error('Failed to create node')
    }
  })
}
</script>

<template>
  <div class="z-50">
    <base-button
      variant="light"
      @click="storedNodesOpen = !storedNodesOpen"
      class="h-9 w-48 gap-2 rounded-lg leading-tight"
      >Nodes
      <chevron-up-icon v-if="storedNodesOpen" class="h-5" />
      <chevron-down-icon v-else class="h-5" />
    </base-button>
    <div
      v-if="storedNodesOpen"
      role="tabpanel"
      class="absolute right-0 top-16 h-[calc(100vh-7rem)] rounded-xl bg-primary-100"
    >
      <nav class="flex gap-2 rounded-xl p-2" role="tablist">
        <base-button
          @click="selectedTab = 0"
          :aria-expanded="selectedTab === 0"
          role="tab"
          class="h-9 flex-grow bg-opacity-0 leading-tight aria-expanded:bg-accent-500 aria-expanded:text-accent-900"
          >Assertions</base-button
        >
        <base-button
          @click="selectedTab = 1"
          :aria-expanded="selectedTab === 1"
          role="tab"
          class="h-9 flex-grow bg-opacity-0 leading-tight aria-expanded:bg-accent-500 aria-expanded:text-accent-900"
          >Actions</base-button
        >
      </nav>
      <div class="flex gap-1 px-2">
        <base-input-field class="h-9 flex-grow" />
        <base-button
          @click="openModal"
          variant="icon"
          aria-label="Create new node"
          class="aspect-square h-9 items-center rounded-lg leading-tight"
        >
          <plus-icon />
        </base-button>
      </div>
      <ul class="m-1 flex flex-col gap-1 pt-0.5">
        <nodes-list-item @update="getNodes" v-for="node in nodes" :key="node.id" :node="node" />
      </ul>
    </div>
    <base-modal id="newNode" submitButtonText="Create" title="Create New Node" @submit="newNode">
      <base-input-field v-model="newNodeModel.label" label="Label" name="label" placeholder="" />
      <base-input-field
        v-model="newNodeModel.node_type"
        label="Node type"
        name="node-type"
        placeholder=""
        inputType="select"
        :options="['Assert', 'Action']"
      />
      <base-input-field
        v-model="newNodeModel.device"
        label="Device"
        name="device"
        placeholder=""
        inputType="number"
      />
      <base-input-field
        v-model="newNodeModel.function"
        inputType="textarea"
        label="Function"
        name="Function"
        placeholder=""
      />
    </base-modal>
  </div>
</template>
