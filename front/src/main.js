import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import axios from 'axios'
import 'aos/dist/aos.css'
import AOS from 'aos'

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);

app.use(router);

app.mount("#app");

AOS.init()

axios.defaults.baseURL = 'http://127.0.0.1:8000'

// 앱 초기화 시 토큰 복구 코드
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const savedToken = localStorage.getItem('token')
if (savedToken) {
  auth.token = savedToken
  auth.isAuthenticated = true
}