<template>
  <div class="auth-container">
    <h2>로그인</h2>

    <!-- Google 로그인 -->
    <div id="google-btn"></div>

    <!-- 카카오 로그인 -->
    <button class="kakao-btn" @click="kakaoLogin">카카오 로그인</button>

    <!-- 일반 로그인 -->
    <RouterLink to="/login" class="btn">일반 로그인</RouterLink>

    <!-- 회원가입 링크 -->
    <p class="signup-msg">
      회원이 아니신가요? <RouterLink to="/signup">회원가입</RouterLink>
    </p>
  </div>
</template>

<script>
import VueJwtDecode from "vue-jwt-decode";

export default {
  mounted() {
    const google = window.google;
    if (google) {
      google.accounts.id.initialize({
        client_id: "854189614623-n676v9ug587tlri6scmhmbrjss7q0vqe.apps.googleusercontent.com",
        callback: this.handleGoogleLogin,
      });
      google.accounts.id.renderButton(
        document.getElementById("google-btn"),
        { theme: "outline", size: "large" }
      );
    }
  },
  methods: {
    handleGoogleLogin(res) {
      const user = VueJwtDecode.decode(res.credential);
      console.log("✅ Google 로그인 완료:", user);
      // 이후 localStorage 저장하거나 Pinia로 관리 가능
      this.$router.push("/");
    },
    kakaoLogin() {
      const REST_API_KEY = "카카오_REST_API_키_여기에";
      const REDIRECT_URI = "http://localhost:5173/oauth/kakao";
      window.location.href =
        `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`;
    },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.kakao-btn {
  background-color: #fee500;
  border: none;
  padding: 0.6rem 1.2rem;
  margin: 1rem 0;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  border-radius: 6px;
}

.btn {
  display: inline-block;
  margin: 1rem 0;
  padding: 0.6rem 1.2rem;
  border: 1px solid #ccc;
  text-decoration: none;
  color: #333;
  border-radius: 6px;
  width: 100%;
  text-align: center;
}

.signup-msg {
  margin-top: 1rem;
  font-size: 0.9rem;
}
</style>
