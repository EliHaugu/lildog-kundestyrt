<script setup lang="ts"></script>

<template>
  <header class="fixed top-0 flex h-12 w-screen gap-44 bg-accent-800">
    <h1 class="ml-8 w-min text-2xl text-accent-400">liltest</h1>
    <ul class="mr-auto flex flex-row gap-4">
      <li>
        <button
          class="rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-white-100 hover:text-accent-900"
        >
          New Device
        </button>
      </li>
      <li>
        <button
          class="rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-white-100 hover:text-accent-900"
        >
          Configure Devices
        </button>
      </li>
      <li>
        <button
          class="rounded-lg px-4 py-1.5 text-white-100 transition-colors duration-200 hover:bg-white-100 hover:text-accent-900"
        >
          API
        </button>
      </li>
    </ul>
  </header>
</template>
