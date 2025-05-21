<template>
  <div class="video-container">
    <video autoplay muted loop playsinline>
      <source src="@/video/mainpagevideo.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  </div>
    <div>
    <h1>Index View</h1>
    <button @click="kakaoLogin">카카오 로그인</button>
  </div>
</template>

<script setup>
const KAKAO_REST_API_KEY = '02549359e75e6f2b90964be5651d7980'
const REDIRECT_URI = 'https://dbgudxkr1.com/oauth/callback'

const kakaoLogin = () => {
  window.location.href =
    `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`
}
</script>

<style scoped>
.video-container {
  width: 100%;
  max-height: 600px;
  overflow: hidden;
}

video {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}
</style>
