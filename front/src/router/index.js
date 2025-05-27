import { createRouter, createWebHistory } from 'vue-router'
import AuthView from '@/views/auth/AuthView.vue'
import SignInView from '@/views/auth/SignInView.vue'
import SignupView from '@/views/auth/SignupView.vue'

import GoogleCallbackView from '@/views/social_callback/GoogleCallbackView.vue'
import KakaoCallback from '@/views/social_callback/KakaoCallback.vue'
import NaverCallback from '@/views/social_callback/NaverCallback.vue'

import DepositView from '@/views/financial/DepositView.vue'
import DepositDetailView from '@/views/financial/DepositDetailView.vue'
import FinancialView from '@/views/financial/FinancialView.vue'
import RecommendView from '@/views/financial/RecommendView.vue'
import StockpriceView from '@/views/financial/StockpriceView.vue'

import CommunityView from '@/views/community/CommunityView.vue'
import CommunityDetailView from '@/views/community/CommunityDetailView.vue'
import CommunityWriteView from '@/views/community/CommunityWriteView.vue'

import MyPageView from '@/views/mypage/MyPageView.vue'
import BookmarkListView from '@/views/mypage/BookmarkListView.vue'
import FavoriteStocksView from '@/views/mypage/FavoriteStocksView.vue'
import UserProfileView from '@/views/mypage/UserProfileView.vue'

import BankSearchView from '@/views/search/BankSearchView.vue'
import NewsSearchView from '@/views/search/NewsSearchView.vue'

import PortfolioView from '@/views/portfolio/PortfolioView.vue'
import SimulationView from '@/views/portfolio/SimulationView.vue'

import IndexView from '@/views/common/IndexView.vue'
import BuyStock from '@/components/BuyStock.vue'
import SellStock from '@/components/SellStock.vue'


const requireAuth = (to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요합니다.')
    return next('/login')
  }
  next()
}

const routes = [
  { path: '/', name: 'home', component: IndexView },
  { path: '/oauth/callback', name: 'kakao-callback', component: KakaoCallback },
  { path: '/auth', name: 'Auth', component: AuthView },
  { path: '/signup', name: 'Signup', component: SignupView },
  { path: '/login', name: 'login', component: SignInView },

  // 마이페이지
  { path: '/mypage', name: 'mypage', component: MyPageView, beforeEnter: requireAuth },
  { path: '/mypage/portfolio', name: 'portfolio', component: PortfolioView, beforeEnter: requireAuth },
  { path: '/mypage/bookmarks', name: 'BookmarkList', component: BookmarkListView, beforeEnter: requireAuth },
  { path: '/mypage/favorites', name: 'FavoriteStocksView', component: FavoriteStocksView, beforeEnter: requireAuth},

  { path: '/bank-search', name: 'BankSearchView', component: BankSearchView },

  // 예적금 비교 페이지 
  { path: '/deposit', name: 'deposit', component: DepositView },
  { path: '/deposit/:id', name: 'Depositdetail', component: DepositDetailView},

  { path: '/financial', name: 'financial', component: FinancialView },
  { path: '/news-summary', name: 'news-summary', component: NewsSearchView },
  { path:'/recommend', name:'Recommend', component: RecommendView },
  { path:'/stock', name:'stock', component: StockpriceView },

  // 시뮬레이션
  { path: '/simulation', name: 'Simulation', component: SimulationView, meta: { requiresAuth: true },},
  { path: '/buy', name: 'BuyStock', component: BuyStock, meta: { requiresAuth: true }, },
  { path: '/sell', name: 'SellStock', component: SellStock, meta: { requiresAuth: true }, },

  // ✅ 커뮤니티
  { path: '/community/articles', name: 'community', component: CommunityView },
  { path: '/community/articles/write', name: 'articlewrite', component: CommunityWriteView, beforeEnter: requireAuth },
  { path: '/community/articles/:id', name: 'articledetail', component: CommunityDetailView },

  // ✅ 프로필 및 팔로우
  { path: '/community/profile/:id', name: 'userprofile', component: UserProfileView },
    // ✅ 소셜 로그인 콜백
  { path: '/oauth/kakao', name: 'kakao-callback', component: KakaoCallback },
  { path: '/oauth/google', name: 'google-callback', component: GoogleCallbackView },
  { path: '/oauth/naver', name: 'naver', component: NaverCallback },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
