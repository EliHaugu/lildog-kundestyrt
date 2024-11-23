<script setup lang="ts">
/**
 * This file contains TypeScript errors, it does not manage to reslove a node type's data property.
 * Every reference points to the correct place, but it is not recognised as so by the compiler.
 * Therefore you will find @ts-ignore comments in the code to allow the code to compile.
 * This is not ideal, but it is a workaround to allow the code to compile; it does not
 * produce any runtime errors relevant to the issue.
 */

import type { NodeProps } from '@vue-flow/core'
import { Handle, Position } from '@vue-flow/core'
import { blue, green, pink, purple } from '@/utils/colorRanges'
import { computed, ref } from 'vue'

import NodeFieldInput from './FlowNodeInput.vue'
import SuccessIcon from '@/icons/SuccessIcon.vue'
import WarningIcon from '@/icons/WarningIcon.vue'
import ErrorIcon from '@/icons/ErrorIcon.vue'
import { updateNode } from '@/services/NodesService'

const props = defineProps<NodeProps>()
const nodeExpanded = ref(false)
const edited = ref(false)


const pickColour = (protocols: string[]) => {
  if (protocols.includes('bluetooth')) {
    return blue[Math.floor(Math.random() * blue.length)]
  } else if (protocols.includes('wifi')) {
    return green[Math.floor(Math.random() * green.length)]
  } else if (protocols.includes('uart')) {
    return pink[Math.floor(Math.random() * pink.length)]
  } else if (protocols.includes('adb')) {
    return purple[Math.floor(Math.random() * purple.length)]
  } else if (protocols.includes('lte')) {
    return green[Math.floor(Math.random() * green.length)]
  }
  return 'grey'
}

const colour = computed(() => pickColour(props.data.communication_protocols || []))

const editedField = (fn: string) => {
  edited.value = true

  updateNode(Number(props.data.id), {
    function: fn
  })
}
</script>

<template>
  <div
    aria-expanded="false"
    class="flow_node flex flex-col gap-1 rounded-xl border-2 bg-primary-200 p-1"
    :class="{
      'border-idle': data.testState === 'idle',
      'border-success': data.testState === 'success',
      'border-warning': data.testState === 'warning',
      'border-error': data.testState === 'failed'
    }"
  >
    <div
      class="flex items-center justify-center rounded-lg"
      :class="{ 'rounded-b-sm': nodeExpanded }"
      :style="{
        backgroundColor: colour
      }"
    >
      <h1
        @click="nodeExpanded = !nodeExpanded"
        class="rounded-lg px-3 py-1 text-lg dark:text-white-100"
      >
        {{
          // @ts-ignore
          data.label
        }}
      </h1>

      <div v-if="data.testState" class="icon-container p-1">
        <success-icon v-if="data.output === true" />
        <error-icon v-else-if="data.output === false" />
        <warning-icon v-else-if="typeof data.output === 'string' && data.output !== ''" />
      </div>
    </div>

    <div v-if="nodeExpanded" class="flex flex-col gap-1">
      <h2
        class="rounded-sm px-3 py-1 text-lg dark:text-white-100"
        :style="{ backgroundColor: colour }"
      >
        {{
          // @ts-ignore
          data.node_type
        }}
      </h2>

      <div class="flex">
        <h3 v-if="data.communicationProtocols" class="text-md text-left dark:text-white-100">
          Connection: BLE
        </h3>
        <h4 v-if="edited" class="text-md ml-auto text-right dark:text-white-100">saved</h4>
      </div>

      <node-field-input
        label="Function"
        :value="
          // @ts-ignore
          data.function
        "
        :colour="colour"
        @edit="editedField"
      />

      <button
        :style="{ backgroundColor: colour }"
        class="flex items-center rounded-b-lg rounded-t-sm px-3 py-2 text-left shadow-md"
      >
        Test Connection
        <div class="ml-auto rounded-sm bg-success px-1">200/OK</div>
      </button>
    </div>

    <Handle type="target" :position="Position.Top" />
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>
