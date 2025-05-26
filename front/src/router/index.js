import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import KakaoCallback from '../views/KakaoCallback.vue'
import AuthView from '@/views/AuthView.vue'
import SignupView from '@/views/SignupView.vue'
import SignInView from '@/views/SignInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import PortfolioView from '@/views/PortfolioView.vue'
import BankSearchView from '@/views/BankSearchView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CommunityDetailView from '@/views/CommunityDetailView.vue'
import CommunityWriteView from '@/views/CommunityWriteView.vue'
import UserProfileView from '@/views/UserProfileView.vue' 
import DepositView from '@/views/DepositView.vue'
import FinancialView from '@/views/FinancialView.vue'
import StockpriceView from '@/views/StockpriceView.vue'
import NewsSearchView from '@/views/NewsSearchView.vue'
import RecommendView from '@/views/RecommendView.vue'
import BookmarkListView from '@/views/BookmarkListView.vue'
import DepositDetailView from '@/views/DepositDetailView.vue'
import FavoriteStocksView from '@/views/FavoriteStocksView.vue'
import SimulationView from '@/views/SimulationView.vue'
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

]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
