import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import KakaoCallback from '../views/KakaoCallback.vue'

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
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
