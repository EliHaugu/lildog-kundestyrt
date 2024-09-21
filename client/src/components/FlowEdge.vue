<script setup>
import { BaseEdge, getSmoothStepPath } from '@vue-flow/core'
import { computed } from 'vue'

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  sourceX: {
    type: Number,
    required: true
  },
  sourceY: {
    type: Number,
    required: true
  },
  targetX: {
    type: Number,
    required: true
  },
  targetY: {
    type: Number,
    required: true
  },
  sourcePosition: {
    type: String,
    required: true
  },
  targetPosition: {
    type: String,
    required: true
  },
  markerEnd: {
    type: String,
    required: false
  }
})

const path = computed(() => getSmoothStepPath(props))
</script>

<script>
export default {
  inheritAttrs: false
}
</script>

<template>
  <BaseEdge :id="id" :style="style" :path="path[0]" :marker-end="markerEnd" />
</template>
