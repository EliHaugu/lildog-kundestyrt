<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Flow } from '@/types/FlowType'
import flowService from '@/services/FlowService'
import NodeService from '@/services/NodeService'
import { fetchDevice } from '@/services/DevicesService'

import FlowCard from '@/components/FlowCard.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseModal from '../components/common/BaseModal.vue'
import { getCategory } from '@/services/CategoryService'

const newFlowStatus = 'Untested'
const newFlowName = ref('')
const searchQuery = ref('')
const flows = ref<Flow[]>([])

const fetchFlows = async () => {
  try {
    const response = await flowService.getFlows()

    const flowsWithConnections = await Promise.all(
      response.map(async (flow: Flow) => {
        const nodeIds = flow.nodes ?? []

        const connections = await Promise.all(
          nodeIds.map(async (nodeId: number) => {
            const node = await NodeService.getNode(nodeId)

            if (node.device) {
              const device = await fetchDevice(node.device)
              if (device && device.category) {
                const category = await getCategory(device.category)

                return {
                  connectionTypes: category.connection_types || [],
                  communicationProtocols: category.communication_protocols || []
                }
              }
            }
            return { connectionTypes: [], communicationProtocols: [] }
          })
        )

        const connectionTypes = Array.from(new Set(connections.flatMap((c) => c.connectionTypes)))
        const communicationProtocols = Array.from(
          new Set(connections.flatMap((c) => c.communicationProtocols))
        )

        return {
          ...flow,
          connectionType: connectionTypes,
          communicationProtocol: communicationProtocols
        }
      })
    )

    flows.value = flowsWithConnections
  } catch (error) {
    console.error('Error fetching flows:', error)
    flows.value = []
  }
}

const filteredFlows = computed(() => {
  if (!searchQuery.value) return flows.value
  return flows.value.filter((flow) =>
    flow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(fetchFlows)

const showNewFlowForm = ref(false)
const createNewFlow = () => {
  ;(document.getElementById('newFlowModal') as HTMLDialogElement).showModal()
}

const addNewFlow = async () => {
  if (!newFlowName.value) return

  const newFlow: Flow = {
    id: '',
    name: newFlowName.value,
    status: newFlowStatus,
    connectionType: [],
    communicationProtocol: [],
    nodes: [],
    edges: []
  }

  try {
    await flowService.createFlow(newFlow)
    await fetchFlows()
    newFlowName.value = ''
    showNewFlowForm.value = false
  } catch (error) {
    console.error('Error creating flow:', error)
  }
}
</script>

<template>
  <main class="flex flex-col gap-4">
    <div class="flex h-10 gap-2">
      <h1 class="p-2 text-xl font-semibold">Test flows</h1>
      <form action="" class="ml-auto w-fit flex-grow">
        <base-input-field
          v-model="searchQuery"
          placeholder="Search for flows"
          class="h-10 rounded-lg"
        />
      </form>
      <base-button class="flex h-10 w-48 flex-shrink-0 items-center gap-2" @click="createNewFlow">
        New flow
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

    <ul class="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      <flow-card
        v-for="flow in filteredFlows"
        :key="flow.id"
        :flow="flow"
        @flowUpdated="fetchFlows"
        :connection-types="flow.connectionType || []"
        :communication-protocols="flow.communicationProtocol || []"
      />
    </ul>
  </main>
</template>
