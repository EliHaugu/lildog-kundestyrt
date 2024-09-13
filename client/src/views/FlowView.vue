<script setup lang="ts">
import { reactive, watch } from 'vue'
import { useRoute } from 'vue-router'

import { listItems } from '@/assets/mock_data'

const route = useRoute()
const item = listItems.find((item) => item.id === route.params.id)
const state = reactive({ id: route.params.id, name: item!.name })

watch(
  () => route.params.id,
  (newId) => {
    state.id = newId
    state.name = listItems.find((item) => item.id === newId)!.name
  }
)
</script>

<template>
  <main class="flex w-screen">
    <h1>{{ state.name }}</h1>
  </main>
</template>
