<script setup lang="ts">
defineProps<{
  to: string
}>()
</script>

<template>
  <router-link
    :to="to"
    :aria-expanded="$route.path.includes(to)"
    class="text-md nav_item__rounded relative flex min-w-max items-center gap-1 rounded-l-xl fill-white-100 py-3 pr-10 text-white-100 hover:cursor-pointer hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:fill-accent-500 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
  >
    <slot />
  </router-link>
</template>
