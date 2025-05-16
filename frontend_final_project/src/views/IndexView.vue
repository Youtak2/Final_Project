<template>
  <div class="video-container">
    <video autoplay muted loop playsinline>
      <source src="@/video/mainpagevideo.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script setup></script>

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
