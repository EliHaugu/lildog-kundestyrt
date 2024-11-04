import { createRouter, createWebHistory } from 'vue-router'

import FlowView from '@/views/FlowView.vue'
import LogView from '@/components/flow/FlowLog.vue'
import CategoryView from '@/views/CategoryView.vue'
import DeviceView from '@/views/DeviceView.vue'
import FlowDetailedView from '@/views/FlowDetailedView.vue'

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
    component: CategoryView
  },
  {
    path: '/categories/:category',
    name: 'category',
    component: DeviceView
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
