<script setup lang="ts">
import type { DeviceCategory } from '@/types/DeviceTypes'
import { ref, computed, onMounted } from 'vue'

import DeviceCategoryCard from '../components/devices/DeviceCategoryCard.vue'
import BaseButton from '../components/common/BaseButton.vue'
import BaseInputField from '@/components/common/BaseInputField.vue'
import BaseModal from '../components/common/BaseModal.vue'

import { fetchCategories, createCategory } from '@/services/CategoryService'

const openModal = () => {
  ;(document.getElementById('newDeviceCategoryModal') as HTMLDialogElement).showModal()
}

const categories = ref<DeviceCategory[]>([])
const newCategoryName = ref('')
const newCategoryConnection = ref('')
const newCategoryCommunication = ref('')
const searchQuery = ref('')

const connectionTypes = ['adb', 'uart']
const communicationProtocols = ['wifi', 'ble', 'lte']

// Fetch categories on component mount
const fetchAllCategories = async () => {
  const data = await fetchCategories()
  if (!data) {
    console.error('Failed to fetch device categories')
    return
  }
  categories.value = data
}

onMounted(fetchAllCategories)

// Add new category and send to server
const addNewDeviceCategory = async () => {
  if (!newCategoryName.value || !newCategoryConnection.value || !newCategoryCommunication.value) {
    if (!newCategoryName.value) {
      console.error('Category name is required')
    }
    if (!newCategoryConnection.value) {
      console.error('Category connection is required')
    }
    if (!newCategoryCommunication.value) {
      console.error('Category communication protocol is required')
    }
    return
  }

  const newDeviceCategory = {
    category_name: newCategoryName.value,
    connection_types: [newCategoryConnection.value],
    communication_protocols: [newCategoryCommunication.value]
  }

  // Send the new category to the server
  const created = await createCategory(newDeviceCategory)
  if (created) {
    await fetchAllCategories() // Refresh the list after adding
    newCategoryName.value = ''
    newCategoryConnection.value = ''
    newCategoryCommunication.value = ''
  } else {
    console.error('Failed to create device category')
  }
}

// Refresh categories when a category is updated or deleted
const refreshCategories = async () => {
  await fetchAllCategories()
}

// Filtered categories based on search query
const filteredCategories = computed(() => {
  return categories.value.filter((category) =>
    category.category_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <main class="flex flex-col gap-4">
    <section class="flex h-10 gap-2">
      <h1 class="flex-shrink-0 p-2 text-xl font-semibold">Device categories</h1>
      <form action="" class="ml-auto flex-grow">
        <base-input-field
          v-model="searchQuery"
          placeholder="Search categories"
          class="h-10 flex-shrink rounded-lg"
        />
      </form>
      <base-button @click="openModal" class="flex h-10 w-48 flex-shrink-0 items-center gap-2">
        New category
      </base-button>
    </section>
    <ul class="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      <device-category-card
        v-for="deviceCategory in filteredCategories"
        :key="deviceCategory.id"
        :deviceCategory="deviceCategory"
        @updated="refreshCategories"
        @deleted="refreshCategories"
      />
    </ul>
    <base-modal
      id="newDeviceCategoryModal"
      title="Create Device Category"
      submit-button-text="Create"
      @submit="addNewDeviceCategory"
    >
      <base-input-field v-model="newCategoryName" label="Name" name="name" placeholder="" />
      <base-input-field
        v-model="newCategoryConnection"
        label="Connection type"
        name="connection-type"
        placeholder=""
        inputType="select"
        :options="connectionTypes"
      />
      <base-input-field
        v-model="newCategoryCommunication"
        label="Communication protocol"
        name="communication-protocol"
        placeholder=""
        inputType="select"
        :options="communicationProtocols"
      />
    </base-modal>
  </main>
</template>
