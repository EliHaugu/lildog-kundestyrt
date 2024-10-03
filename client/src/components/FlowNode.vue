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
      class="flex items-center justify-center "
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

      <div v-if="nodeTestState" class="icon-container p-1" >
        <svg
          v-if="nodeTestState === 'success'"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 -960 960 960"
        >
          <path d="M382-240 154-468l57-57 171 171 367-367 57 57z" />
        </svg>
        <svg
          v-if="nodeTestState === 'warning'"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 -960 960 960"
        >
          <path d="M440-400v-360h80v360zm0 200v-80h80v80z" />
        </svg>
        <svg
          v-if="nodeTestState === 'error'"
          width="24"
          height="24"
          viewBox="0 0 16 16"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M8.6 1c1.6.1 3.1.9 4.2 2 1.3 1.4 2 3.1 2 5.1 0 1.6-.6 3.1-1.6 4.4-1 1.2-2.4 2.1-4 2.4-1.6.3-3.2.1-4.6-.7-1.4-.8-2.5-2-3.1-3.5C.9 9.2.8 7.5 1.3 6c.5-1.6 1.4-2.9 2.8-3.8C5.4 1.3 7 .9 8.6 1zm.5 12.9c1.3-.3 2.5-1 3.4-2.1.8-1.1 1.3-2.4 1.2-3.8 0-1.6-.6-3.2-1.7-4.3-1-1-2.2-1.6-3.6-1.7-1.3-.1-2.7.2-3.8 1-1.1.8-1.9 1.9-2.3 3.3-.4 1.3-.4 2.7.2 4 .6 1.3 1.5 2.3 2.7 3 1.2.7 2.6.9 3.9.6zM7.9 7.5L10.3 5l.7.7-2.4 2.5 2.4 2.5-.7.7-2.4-2.5-2.4 2.5-.7-.7 2.4-2.5-2.4-2.5.7-.7 2.4 2.5z"
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
