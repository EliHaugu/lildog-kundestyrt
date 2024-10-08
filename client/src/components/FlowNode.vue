<script setup lang="ts">
import type { CustomData } from '@/types/nodeType'
import { Handle, Position } from '@vue-flow/core'
import type { NodeProps } from '@vue-flow/core'
import { blue, green, pink, purple } from '@/utils/colorRanges'
import { ref } from 'vue'
import NodeFieldInput from './node/FieldInput.vue'

const props = defineProps<NodeProps<CustomData>>()
const nodeTestState = ref(props.data.testState)
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

const colour = pickColour(props!.data.connection!)

const editedField = () => {
  edited.value = true
}

const getKeysByValue = (value: string) => {
  const fields = props.data.fields as { [key: string]: string } | undefined
  return Object.keys(fields!).find((key) => fields![key] === value)
}
</script>

<template>
  <div
    aria-expanded="false"
    class="flow_node flex flex-col gap-1 rounded-xl border-2 border-idle bg-primary-200 p-1"
    :class="{
      'border-success': nodeTestState === 'success',
      'border-warning': nodeTestState === 'warning',
      'border-error': nodeTestState === 'error'
    }"
  >
    <div
      class="flex items-center justify-center"
      :style="{
        backgroundColor: colour,
        borderTopRightRadius: '8px',
        borderTopLeftRadius: '8px',
        borderBottomRightRadius: nodeExpanded ? '2px' : '8px',
        borderBottomLeftRadius: nodeExpanded ? '2px' : '8px'
      }"
    >
      <h1
        @click="nodeExpanded = !nodeExpanded"
        class="rounded-lg px-3 py-1 text-lg dark:text-white-100"
      >
        {{ data.label }}
      </h1>

      <div v-if="nodeTestState" class="icon-container p-1">
        <svg
          v-if="nodeTestState === 'success'"
          xmlns="http://www.w3.org/2000/svg"
          width="28"
          height="28"
          viewBox="0 -960 960 960"
          class="rounded-md border bg-success"
          fill="#00312F"
        >
          <path d="M382-240 154-468l57-57 171 171 367-367 57 57z" />
        </svg>
        <svg
          v-if="nodeTestState === 'warning'"
          xmlns="http://www.w3.org/2000/svg"
          width="28"
          height="28"
          viewBox="0 -960 960 960"
          class="rounded-md border bg-warning"
          fill="#00312F"
        >
          <path d="M440-400v-360h80v360zm0 200v-80h80v80z" />
        </svg>
        <svg
          v-if="nodeTestState === 'error'"
          width="28"
          height="28"
          viewBox="0 0 15 15"
          xmlns="http://www.w3.org/2000/svg"
          class="rounded-md border bg-[#FF5B49]"
          fill="#00312F"
        >
          <path
            d="M12.8536 2.85355C13.0488 2.65829 13.0488 2.34171 12.8536 2.14645C12.6583 1.95118 12.3417 1.95118 12.1464 2.14645L7.5 6.79289L2.85355 2.14645C2.65829 1.95118 2.34171 1.95118 2.14645 2.14645C1.95118 2.34171 1.95118 2.65829 2.14645 2.85355L6.79289 7.5L2.14645 12.1464C1.95118 12.3417 1.95118 12.6583 2.14645 12.8536C2.34171 13.0488 2.65829 13.0488 2.85355 12.8536L7.5 8.20711L12.1464 12.8536C12.3417 13.0488 12.6583 13.0488 12.8536 12.8536C13.0488 12.6583 13.0488 12.3417 12.8536 12.1464L8.20711 7.5L12.8536 2.85355Z"
          />
        </svg>
      </div>
    </div>

    <div v-if="nodeExpanded" class="flex flex-col gap-1">
      <h2
        class="rounded-sm px-3 py-1 text-lg dark:text-white-100"
        :style="{ backgroundColor: colour }"
      >
        {{ data.type }}
      </h2>

      <div class="flex">
        <h3 class="text-md text-left dark:text-white-100">Connection: {{ data.connection }}</h3>
        <h4 v-if="edited" class="text-md ml-auto text-right dark:text-white-100">saved</h4>
      </div>

      <ul class="flex flex-col gap-1">
        <li v-for="field in data.fields" :key="field">
          <node-field-input
            :label="getKeysByValue(field!)"
            :value="field"
            :colour="colour"
            @edit="editedField"
          />
        </li>
      </ul>

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
