<script setup lang="ts">
import BaseButton from '../common/BaseButton.vue'
defineProps(['error'])
defineEmits(['close'])
</script>
<template>
  <div class="mt-2 flex items-center gap-2 rounded-xl bg-error p-2 text-accent-900">
    <h1>Error:</h1>
    <p>{{ error }}</p>
    <base-button class="ml-auto h-8 items-center" @click="$emit('close')">Close</base-button>
  </div>
</template>
