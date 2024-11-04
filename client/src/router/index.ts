import { createRouter, createWebHistory } from 'vue-router'

import FlowView from '@/views/FlowView.vue'
import LogView from '@/components/flow/FlowLog.vue'
import FlowDetailedView from '@/views/FlowDetailedView.vue'
import DeviceCategoriesView from '@/views/DeviceCategoriesView.vue'
import DeviceCategoryView from '@/views/DeviceCategoryView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: FlowView
  },
  {
    path: '/flow',
    name: 'flows',
    component: FlowView
  },
  {
    path: '/flow/:id',
    name: 'flow',
    component: FlowDetailedView
  },
  {
    path: '/flow/:id/log',
    name: 'log',
    component: LogView,
    props: true
  },
  {
    path: '/categories',
    name: 'categories',
    component: DeviceCategoriesView
  },
  {
    path: '/categories/:id',
    name: 'category',
    component: DeviceCategoryView
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
