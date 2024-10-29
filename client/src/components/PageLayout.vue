<script setup lang="ts">
import Navigation from '@/components/PageNavigation.vue'
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-accent-800">
    <navigation />
    <slot></slot>
  </div>
</template>
