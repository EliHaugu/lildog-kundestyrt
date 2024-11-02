<template>
  <teleport to="body">
    <dialog
      :aria-label="title"
      :id="id"
      class="absolute dark:text-white-100 top-1/2 z-50 -translate-y-1/2 rounded-xl bg-primary-100 p-4 shadow-md"
    >
      <form method="dialog" @submit.prevent="submit" class="flex w-96 flex-col gap-2">
        <h3 v-if="title" class="text-xl font-semibold">{{ title }}</h3>
        <slot />
        <div class="flex gap-2">
          <base-button class="flex-grow" type="button" @click="close" :variant="'outline'"
            >Cancel</base-button
          >
          <base-button class="flex-grow" type="submit">{{ submitButtonText }}</base-button>
        </div>
      </form>
    </dialog>
  </teleport>
</template>

<script setup lang="ts">
import BaseButton from './BaseButton.vue'

const props = defineProps<{
  id: string
  submitButtonText: string
  title?: string
  onSubmit: () => void
}>()

const close = () => {
  ;(document.getElementById(props.id) as HTMLDialogElement).close()
}

const submit = () => {
  props.onSubmit()
  close()
}
</script>

<style scoped>
dialog[open]::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  height: 100vh;
  width: 100vw;
}
</style>
