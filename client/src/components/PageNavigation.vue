<script setup lang="ts">
import { listItems } from '@/assets/mock_data'
import BaseButton from './BaseButton.vue'
</script>

<template>
  <nav id="header__rounded_corner" class="fixed left-0 top-12 h-screen w-64 bg-accent-800 pl-4">
    <h2 class="pl-4 text-lg text-white-100">Stored Flows</h2>

    <ul class="relative flex max-h-[calc(100vh-9.5rem)] flex-col gap-2 overflow-y-scroll py-4">
      <li
        v-bind:key="item.id"
        v-for="item in listItems"
        :aria-expanded="item.id === $route.params.id"
        class="text-md nav_item__rounded relative z-10 rounded-l-xl text-white-100 hover:z-50 hover:cursor-pointer hover:bg-primary-300 hover:text-accent-900 hover:shadow-xl hover:transition-colors hover:duration-200 aria-expanded:bg-primary-200 aria-expanded:text-accent-900 aria-expanded:duration-0 dark:hover:bg-primary-200 dark:hover:text-white-100 dark:aria-expanded:text-white-100"
      >
        <router-link
          :to="`/flow/${item.id}`"
          tabindex="2"
          class="line-clamp-1 max-w-56 text-ellipsis py-1.5 pl-4 pr-2 leading-10"
          >{{ item.name }}</router-link
        >
      </li>
    </ul>
    <BaseButton
      variant="outline"
      tabindex="3"
      class="absolute bottom-16 flex px-14 py-2.5 transition-colors"
      >New Flow
      <svg
        width="24"
        height="24"
        viewBox="0 0 15 15"
        class="ml-4"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M12 13C12.5523 13 13 12.5523 13 12V3C13 2.44771 12.5523 2 12 2H3C2.44771 2 2 2.44771 2 3V6.5C2 6.77614 2.22386 7 2.5 7C2.77614 7 3 6.77614 3 6.5V3H12V12H8.5C8.22386 12 8 12.2239 8 12.5C8 12.7761 8.22386 13 8.5 13H12ZM9 6.5C9 6.5001 9 6.50021 9 6.50031V6.50035V9.5C9 9.77614 8.77614 10 8.5 10C8.22386 10 8 9.77614 8 9.5V7.70711L2.85355 12.8536C2.65829 13.0488 2.34171 13.0488 2.14645 12.8536C1.95118 12.6583 1.95118 12.3417 2.14645 12.1464L7.29289 7H5.5C5.22386 7 5 6.77614 5 6.5C5 6.22386 5.22386 6 5.5 6H8.5C8.56779 6 8.63244 6.01349 8.69139 6.03794C8.74949 6.06198 8.80398 6.09744 8.85143 6.14433C8.94251 6.23434 8.9992 6.35909 8.99999 6.49708L8.99999 6.49738"
          fill="#014848"
        />
      </svg>
    </BaseButton>
  </nav>
</template>
