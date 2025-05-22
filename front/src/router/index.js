import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import KakaoCallback from '../views/KakaoCallback.vue'
import AuthView from '@/views/AuthView.vue'
import SignupView from '@/views/SignupView.vue'
import SignInView from '@/views/SignInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import PortfolioView from '@/views/PortfolioView.vue'
import BankSearchView from '@/views/BankSearchView.vue'
import DepositView from '@/views/DepositView.vue'
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
  },
  { path: '/login', name: 'login', component: SignInView },
  {  path: '/mypage',
  name: 'mypage',
  component: MyPageView}, 
  {
    path:'/mypage/portfolio',
    name:'portfolio',
    component:PortfolioView,
  },
    {
    path: '/bank-search',
    name: 'BankSearchView',
    component: BankSearchView,
  },
  // 금융 상품 목록
  {
    path: '/deposit',
    name: 'deposit',
    component: DepositView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
