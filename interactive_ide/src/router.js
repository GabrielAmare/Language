import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ide',
      name: 'ide',
      component: () => import('./views/IdeView.vue')
    },
    {
      path: '/langs',
      name: 'langs',
      component: () => import('./views/LangView.vue')
    }
  ]
})

export default router
