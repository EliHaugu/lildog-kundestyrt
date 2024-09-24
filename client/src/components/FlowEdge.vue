<script setup lang="ts">
import { BaseEdge, getSmoothStepPath, Position } from '@vue-flow/core'
import { computed } from 'vue'
import type { PropType } from 'vue'

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
    type: String as PropType<Position>,
    required: true
  },
  targetPosition: {
    type: String as PropType<Position>,
    required: true
  },
  markerEnd: {
    type: String,
    required: false
  }
})

const path = computed(() => getSmoothStepPath(props))
</script>

<script lang="ts">
export default {
  inheritAttrs: false
}
</script>

<template>
  <BaseEdge :id="id" :path="path[0]" :marker-end="markerEnd" />
</template>
