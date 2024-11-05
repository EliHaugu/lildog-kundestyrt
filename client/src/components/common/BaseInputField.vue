<script setup lang="ts">
import { computed, useAttrs } from 'vue'

const props = defineProps({
  inputType: {
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
  },
  label: {
    type: String,
    default: ''
  },
  options: {
    type: Array as () => string[],
    default: () => ['Option 1', 'Option 2', 'Option 3']
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

const inputComponent = computed(() => {
  switch (props.inputType) {
    case 'textarea':
      return 'textarea'
    case 'select':
      return 'select'
    default:
      return 'input'
  }
})
</script>

<template>
  <div class="flex flex-col gap-1">
    <label v-if="label">{{ label }}</label>
    <component
      :is="inputComponent"
      v-if="inputType !== 'select'"
      :type="inputType"
      :placeholder="placeholder"
      :class="computedClass"
      :value="modelValue"
      @input="onInput"
      v-bind="$attrs"
      v-on="listeners"
    />
    <component
      :is="inputComponent"
      v-else
      :placeholder="placeholder"
      :class="computedClass"
      :value="modelValue"
      @input="onInput"
      v-bind="$attrs"
      v-on="listeners"
    >
      <option value="" disabled selected>Select</option>
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </component>
  </div>
</template>
