import { createRouter, createWebHistory } from 'vue-router'

import LandingView from '@//views/LandingView.vue'
import FlowView from '@/views/FlowView.vue'
import LogView from '@/components/flow/FlowLog.vue'
import DevicesView from '@/views/DevicesView.vue'
import ApiView from '@/views/ApiView.vue'
import NewDeviceView from '@/views/NewDeviceView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingView
  },
  {
    path: '/flow/:id',
    name: 'flow',
    component: FlowView
  },
  {
    path: '/flow/:id/log',
    name: 'log',
    component: LogView,
    props: true
  },
  {
    path: '/new',
    name: 'new',
    component: NewDeviceView
  },
  {
    path: '/devices',
    name: 'devices',
    component: DevicesView
  },
  {
    path: '/api',
    name: 'api',
    component: ApiView
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
