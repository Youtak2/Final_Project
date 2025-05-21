import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import KakaoCallback from '../views/KakaoCallback.vue'
import AuthView from '@/views/AuthView.vue'
import SignupView from '@/views/SignupView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: IndexView
  },
{
  path: '/oauth/callback',
  name: 'kakao-callback',
  component: KakaoCallback,
}
,
  {
    path: '/auth',
    name: 'Auth',
    component: AuthView,
  },

  {
    path:'/signup',
    name:'Signup',
    component:SignupView,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
