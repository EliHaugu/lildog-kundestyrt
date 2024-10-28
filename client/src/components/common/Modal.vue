<template>
  <div v-if="showModal" class="fixed inset-0 bg-[#000000] opacity-30"></div>
  <form
    v-if="showModal"
    class="absolute left-[50%] top-[50%] z-10 flex w-96 translate-x-[-50%] translate-y-[-50%] transform flex-col gap-6 rounded-xl bg-primary-100 p-4 pt-6 shadow-md"
    @submit="handleSubmit"
  >
    <h1 v-if="title" class="text-xl font-semibold">{{ title }}</h1>
    <div class="flex flex-col gap-3">
      <slot></slot>
    </div>
    <div class="flex justify-between gap-4">
      <base-button type="button" @click="$emit('close')" :variant="'outline'">Cancel</base-button>
      <base-button type="submit">{{ submitButtonText }}</base-button>
    </div>
  </form>
</template>

<script setup lang="ts">
import BaseButton from './BaseButton.vue';

const props = defineProps<{
  showModal: boolean,
  submitButtonText: string,
  title?: string,
  onSubmit: () => void
}>()

const emit = defineEmits(['submit', 'close'])

const handleSubmit = (event: Event) => {
  event.preventDefault()
  emit('submit')
  emit('close')
} 
</script>
