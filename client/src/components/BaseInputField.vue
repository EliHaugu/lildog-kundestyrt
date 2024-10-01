<template>
  <input
    :type="type"
    :placeholder="placeholder"
    :class="computedClass"
    v-bind="$attrs"
    v-on="listeners"
  />
</template>

<script setup lang="ts">
import { computed, useAttrs } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  customClass: {
    type: String,
    default: ''
  }
})

const attrs = useAttrs()
const listeners = attrs.on || {}

const computedClass = computed(() => {
  return `mb-4 w-auto flex-grow rounded-lg border border-accent-600 bg-primary-200 px-4 py-2 ${props.customClass}`
})
</script>

<style scoped></style>
