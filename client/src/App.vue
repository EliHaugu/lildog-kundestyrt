<script setup lang="ts">
import Layout from '@/components/PageLayout.vue'
</script>
<template>
  <Layout>
    <RouterView class="z-10 my-2 mr-2 flex-grow rounded-2xl bg-white-200 p-4 dark:bg-accent-900" />
  </Layout>
</template>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/minimap/dist/style.css';
</style>
