<script setup lang="ts">
/**
 * This file contains TypeScript errors, it does not manage to reslove a node type's data property.
 * Every reference points to the correct place, but it is not recognised as so by the compiler.
 * Therefore you will find @ts-ignore comments in the code to allow the code to compile.
 * This is not ideal, but it is a workaround to allow the code to compile; it does not
 * produce any runtime errors relevant to the issue.
 */

import type { NodeProps } from '@vue-flow/core'
import type { BaseNode } from '@/types/NodeType'
import { Handle, Position } from '@vue-flow/core'
import { blue, green, pink, purple } from '@/utils/colorRanges'
import { ref } from 'vue'

import NodeFieldInput from './FlowNodeInput.vue'
import SuccessIcon from '@/icons/SuccessIcon.vue'
import WarningIcon from '@/icons/WarningIcon.vue'
import ErrorIcon from '@/icons/ErrorIcon.vue'

defineProps<NodeProps<BaseNode>>()
const nodeTestState = ref('success')
const nodeExpanded = ref(false)
const edited = ref(false)

const pickColour = (connectionType: string) => {
  switch (connectionType) {
    case 'BLE':
      return blue[Math.floor(Math.random() * blue.length)]
    case 'LTE':
      return green[Math.floor(Math.random() * green.length)]
    case 'WiFi':
      return pink[Math.floor(Math.random() * pink.length)]
    case 'ADE':
      return purple[Math.floor(Math.random() * purple.length)]
    default:
      break
  }
}

const colour = pickColour('WiFi')

const editedField = () => {
  edited.value = true
}
</script>

<template>
  <div
    aria-expanded="false"
    class="flow_node flex flex-col gap-1 rounded-xl border-2 bg-primary-200 p-1"
    :class="{
      'border-idle': nodeTestState === 'idle',
      'border-success': nodeTestState === 'success',
      'border-warning': nodeTestState === 'warning',
      'border-error': nodeTestState === 'error'
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

      <div v-if="nodeTestState" class="icon-container p-1">
        <success-icon v-if="nodeTestState === 'success'" />
        <warning-icon v-if="nodeTestState === 'warning'" />
        <error-icon v-if="nodeTestState === 'error'" />
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
        <h3 class="text-md text-left dark:text-white-100">Connection: BLE</h3>
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
