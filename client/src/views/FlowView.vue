<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Flow } from '@/types/FlowType'
import FlowCard from '@/components/FlowCard.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import flowService from '@/services/FlowService'
import NodeService from '@/services/NodeService'
import { fetchDevice } from '@/services/DevicesService'
import CategoryService from '@/services/CategoryService'
import Modal from '../components/common/Modal.vue'

const searchQuery = ref('')
const flows = ref<Flow[]>([])

// Function to fetch flows from the API
// Function to fetch flows from the API
const fetchFlows = async () => {
  try {
    const response = await flowService.getFlows()

    const flowsWithConnections = await Promise.all(
      response.map(async (flow: Flow) => {
        const nodeIds = flow.nodes ?? []

        // Retrieve each node's device and category connection types and communication protocols
        const connections = await Promise.all(
          nodeIds.map(async (nodeId: number) => {
            const node = await NodeService.getNode(nodeId)

            // Get device and category data if device is present
            if (node.device) {
              const device = await fetchDevice(node.device)
              if (device && device.category) {
                const category = await CategoryService.getCategory(device.category)
                return (category.connection_types || []).concat(
                  category.communication_protocols || []
                )
              }
            }
            return []
          })
        )

        // Flatten and deduplicate the combined list of connections for each flow
        const combinedData = Array.from(new Set(connections.flat()))

        return {
          ...flow,
          combinedData // Add combined data
        }
      })
    )

    flows.value = flowsWithConnections
  } catch (error) {
    console.error('Error fetching flows:', error)
    flows.value = []
  }
}

// Computed property to filter flows based on search query
const filteredFlows = computed(() => {
  if (!searchQuery.value) return flows.value
  return flows.value.filter((flow) =>
    flow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Call fetchFlows when the component is mounted
onMounted(fetchFlows)

// New form functionality
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

const addNewFlow = async () => {
  if (!newFlowName.value) return

  const newFlow: Flow = {
    id: '', // backend generates ID
    name: newFlowName.value,
    status: newFlowStatus,
    connectionType: [],
    conmmunicationProtocol: [],
    nodes: [],
    edges: []
  }

  try {
    await flowService.createFlow(newFlow)
    console.log('Flow created')
    await fetchFlows() // Re-fetch flows after adding a new flow
    newFlowName.value = ''
    showNewFlowForm.value = false
  } catch (error) {
    console.error('Error creating flow:', error)
  }
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

    <!-- New Flow Form -->
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

    <!-- Flow List Display -->
    <ul class="mr-4 flex flex-wrap gap-4">
      <flow-card
        v-for="flow in filteredFlows"
        :key="flow.id"
        :flow="flow"
        @flowUpdated="fetchFlows"
        :connection-types="flow.connectionType || []"
      />
    </ul>
  </main>
</template>
