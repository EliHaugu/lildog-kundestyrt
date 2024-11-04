<script setup lang="ts">
import { ref, inject, computed, type Ref } from 'vue'
import type { Flow, Flows } from '@/types/FlowType'
import FlowCard from '@/components/FlowCard.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseModal from '../components/common/BaseModal.vue'

const searchQuery = ref('')

const flows = inject<Ref<Flows>>('flows', ref([]))

const filteredFlows = computed(() => {
  console.log(flows.value)
  if (!searchQuery.value) return flows.value
  return flows.value.filter((flow) =>
    flow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const newFlowStatus = 'Untested'
const newFlowName = ref('')

const createNewFlow = () => {
  ;(document.getElementById('newFlowModal') as HTMLDialogElement).showModal()
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
}
</script>

<template>
  <main class="flex flex-col gap-6">
    <div class="flex h-10 gap-2">
      <h1 class="p-2 pt-1 text-2xl font-semibold">Test flows</h1>
      <form action="" class="ml-auto w-fit flex-grow">
        <base-input-field v-model="searchQuery" placeholder="Search for flows" class="rounded-lg" />
      </form>
      <base-button class="w-48 items-center rounded-lg" @click="createNewFlow">
        New flow
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </div>

    <base-modal
      id="newFlowModal"
      submitButtonText="Create"
      title="Create New Flow"
      @submit="addNewFlow"
    >
      <base-input-field v-model="newFlowName" label="Flow name" />
    </base-modal>

    <ul class="mr-4 flex flex-wrap gap-2">
      <flow-card v-for="flow in filteredFlows" :key="flow.id" :flow="flow" />
    </ul>
  </main>
</template>
