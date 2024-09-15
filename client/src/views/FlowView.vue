<script setup lang="ts">

import { listItems } from '@/assets/mock_data'
import LogView from '../components/FlowLog.vue';
import { ref } from 'vue';

const displayLog = ref(false);

</script>

<template>
  <main class="flex flex-col">
     <h1>{{ listItems.find((item) => item.id === $route.params.id)?.name }} </h1>


    <LogView :show=displayLog />
    <button @click="displayLog = !displayLog" class="absolute bottom-4">Test</button>

  </main>
</template>
