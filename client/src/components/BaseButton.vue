<template>
  <button
    :class="[
      'rounded-xl px-4 py-2 shadow-md',
      variantClass,
      sizeClass,
      { 'hover:bg-opacity-80': hoverEffect, 'cursor-not-allowed opacity-50': disabled }
    ]"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary'
  },
  size: {
    type: String,
    default: 'md'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  hoverEffect: {
    type: Boolean,
    default: true
  },
  shadow: {
    type: String,
    default: 'md'
  }
})

const emits = defineEmits(['click'])

const handleClick = (event: Event) => {
  event.preventDefault()
  if (!props.disabled) {
    emits('click', event)
  }
}

// Compute the button variant class
const variantClass = computed(() => {
  switch (props.variant) {
    case 'outline':
      return 'bg-primary-200 text-bg-700 transition-colours duration-200 hover:bg-accent-500 border border-accent-600'
    case 'secondary':
      return 'bg-accent-400 text-bg-700 '
    default:
      return 'bg-accent-600 text-white-100'
  }
})

// Compute the button size class
const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'text-sm px-3 py-1'
    case 'lg':
      return 'text-lg px-6 py-3'
    default:
      return 'text-md px-4 py-2'
  }
})
</script>

<style scoped></style>
