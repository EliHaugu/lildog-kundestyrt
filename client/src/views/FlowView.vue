<script setup lang="ts">
import { ref, inject, computed, type Ref } from 'vue'
import type { Flows } from '@/types/FlowType'
import FlowCard from '@/components/FlowCard.vue'
import BaseInputField from '@/components/BaseInputField.vue'
import BaseButton from '@/components/BaseButton.vue'

const searchQuery = ref('')

const flows = inject<Ref<Flows>>('flows', ref([]))

const filteredFlows = computed(() => {
  console.log(flows.value)
  if (!searchQuery.value) return flows.value
  return flows.value.filter((flow) =>
    flow.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <main class="flex flex-col gap-6">
    <section class="flex h-10 gap-2">
      <h1 class="p-2 pt-1 text-2xl font-semibold">Configure flows</h1>
      <form action="" class="ml-auto flex flex-grow gap-4">
        <base-input-field v-model="searchQuery" placeholder="Search for flows" class="rounded-lg" />
      </form>
      <base-button class="mr-4 w-fit items-center rounded-lg">
        New flow
        <i class="mdi mdi-plus p-1 text-xl"></i>
      </base-button>
    </section>
    <ul class="mr-4 flex flex-wrap gap-4">
      <flow-card v-for="flow in filteredFlows" :key="flow.id" :flow="flow" />
    </ul>
  </main>
</template>
