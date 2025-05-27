<template>
  <div class="video-container">
    <video autoplay muted loop playsinline>
      <source src="/video/mainpagevideo.mp4" type="video/mp4" />
    </video>
  </div>
    <div>
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
.video-wrapper {
  position: relative;
  width: 100%;
  height: 600px;
  overflow: hidden;
}

.video-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ✅ 영상 위에 올리는 영역 */
.video-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}
</style>
