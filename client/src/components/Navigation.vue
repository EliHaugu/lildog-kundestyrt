<script setup lang="ts">
const mockNavItems = [
  {
    id: 1,
    name: 'Test button activates backend and light'
  },
  {
    id: 2,
    name: 'Test light switches'
  },
  {
    id: 3,
    name: 'Test GPS location tracker turns on'
  },
  {
    id: 4,
    name: 'Test interface updates on request'
  }
]
</script>

<template>
  <nav id="header__rounded_corner" class="fixed left-0 top-12 h-screen w-64 bg-accent-800 pl-4">
    <h2 class="pb-3 pl-4 text-lg text-white-100">Test Flows</h2>

    <ul class="flex flex-col gap-2">
      <li
        v-for="item in mockNavItems"
        class="text-md nav_item__rounded relative rounded-l-xl py-3 pl-4 pr-2 text-white-100 hover:cursor-pointer hover:bg-white-200 hover:text-accent-900"
      >
        <p class="line-clamp-1 max-w-56 text-ellipsis">{{ item.name }}</p>
      </li>
    </ul>
    <button
      class="absolute bottom-16 mx-auto w-56 rounded-xl bg-white-200 px-4 py-2.5 transition-colors duration-200 hover:cursor-pointer hover:bg-accent-500"
    >
      New Flow
    </button>
  </nav>
</template>
