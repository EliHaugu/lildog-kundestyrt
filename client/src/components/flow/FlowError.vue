<script setup lang="ts">
import BaseButton from '../common/BaseButton.vue';
defineProps(['error'])
defineEmits(['close'])
</script>
<template>
    <div class="rounded-xl p-2 mt-2 items-center flex gap-2 bg-error text-accent-900 ">
        <h1>Error:</h1>
        <p>{{ error }}</p>
        <base-button class="ml-auto h-8 items-center" @click="$emit('close')">Close</base-button>
    </div>
</template>