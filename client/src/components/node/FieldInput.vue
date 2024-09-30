<script setup lang="ts">
defineProps({
  colour: String,
  label: String,
  value: String
})

defineEmits(['edit'])
</script>

<template>
  <span class="flex items-center gap-1">
    <label :for="label" class="text-md dark:text-white-100">{{ label }}:</label>
    <input
      :name="label"
      type="text"
      :value="value"
      :style="{ backgroundColor: colour }"
      class="ml-auto rounded-sm px-2 py-1"
      @input="$emit('edit')"
    />
  </span>
</template>
