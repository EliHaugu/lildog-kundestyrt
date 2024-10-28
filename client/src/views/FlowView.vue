<script setup lang="ts">
import { ref, inject, computed, type Ref } from 'vue'
import type { Flow, Flows } from '@/types/FlowType'
import FlowCard from '@/components/FlowCard.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import Modal from '../components/common/Modal.vue'

const searchQuery = ref('')

const flows = inject<Ref<Flows>>('flows', ref([]))

const filteredFlows = computed(() => {
  console.log(flows.value)
  if (!searchQuery.value) return flows.value
  return flows.value.filter((flow) =>
    flow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// new form functionality

const showNewFlowForm = ref(false)
const newFlowStatus = 'Untested'
const newFlowName = ref('')

const createNewFlow = () => {
  showNewFlowForm.value = true
}

const cancelNewFlow = () => {
  newFlowName.value = ''
  showNewFlowForm.value = false
}

const addNewFlow = () => {
  if (!newFlowName.value) return

  const newFlow: Flow = {
    id: (flows.value.length + 1).toString(),
    name: newFlowName.value + (flows.value.length + 1).toString(),
    status: newFlowStatus,
    connectionTypes: [],
    nodes: [],
    edges: []
  }

  flows.value.push(newFlow)

  newFlowName.value = ''
  showNewFlowForm.value = false
}
</script>

<template>
  <main class="flex flex-col gap-6">
    <div class="flex h-10 gap-2">
      <h1 class="p-2 pt-1 text-2xl font-semibold">Test flows</h1>
      <form action="" class="ml-auto flex flex-grow gap-4 pr-2">
        <base-input-field v-model="searchQuery" placeholder="Search for flows" class="rounded-lg" />
      </form>
      <base-button class="mr-4 w-fit items-center rounded-lg" @click="createNewFlow">
        New flow
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </div>

    <modal
      :showModal="showNewFlowForm"
      submitButtonText="Create"
      title="Create New Flow"
      @submit="addNewFlow"
      @close="cancelNewFlow"
    >
      <base-input-field v-model="newFlowName" label="Flow name" />
    </modal>

    <div
      v-if="showNewFlowForm"
      class="fixed inset-0 bg-[#000000] opacity-30"
      style="z-index: 2"
    ></div>

    <ul class="mr-4 flex flex-wrap gap-4">
      <flow-card v-for="flow in filteredFlows" :key="flow.id" :flow="flow" />
    </ul>
  </main>
</template>
