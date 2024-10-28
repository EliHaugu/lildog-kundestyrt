<template>
  <input
    :type="type"
    :placeholder="placeholder"
    :class="computedClass"
    :value="modelValue"
    @input="onInput"
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
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const attrs = useAttrs()
const listeners = attrs.on || {}

const computedClass = computed(() => {
  return `w-auto flex-grow rounded-lg border border-accent-600 bg-primary-200 px-4 py-2 ${props.customClass}`
})

const emit = defineEmits(['update:modelValue'])
const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped></style>
