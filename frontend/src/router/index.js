import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/verify',
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/sign',
      name: 'sign_document',
      component: () => import('../views/SignDocumentView.vue'),
    },
    {
      path: '/verify',
      name: 'verify_document',
      component: () => import('../views/VerifyDocumentView.vue'),
    },
  ],
})

export default router
