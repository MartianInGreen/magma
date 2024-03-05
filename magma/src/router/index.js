import { createRouter, createWebHistory } from 'vue-router'
import WelcomeView from '../views/WelcomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: WelcomeView
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'Signup',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/notes',
      name: 'Notes',
      component: () => import('../views/NotesView.vue')
    }
  ]
})

export default router
