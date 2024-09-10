<script setup lang="ts"></script>

<template>
  <header class="fixed top-0 flex h-12 w-screen gap-40 bg-accent-800">
    <h1 class="ml-8 w-min text-2xl text-accent-400">liltest</h1>
    <ul class="ml-2 mr-auto flex flex-row gap-4">
      <li v-for="item in ['New Device', 'Configure Devices', 'API']">
        <button
          tabindex="1"
          class="rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-white-100 hover:text-accent-900 hover:shadow-lg"
        >
          {{ item }}
        </button>
      </li>
    </ul>
  </header>
</template>
