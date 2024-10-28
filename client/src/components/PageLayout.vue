<script setup lang="ts">
import Navigation from '@/components/PageNavigation.vue'
</script>

<template>
  <div class="h-full bg-accent-800 flex">
    <navigation />
    <slot></slot>
  </div>
</template>
