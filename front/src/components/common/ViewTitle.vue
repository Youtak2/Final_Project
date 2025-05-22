<template>
  <v-row>
    <v-col cols="12">
      <div class="title-wrapper text-center">
        <h1 class="text-h3 font-weight-bold mb-2 primary--text">
          {{ title }}
        </h1>
        <div class="subtitle text-subtitle-1 grey--text">{{ subtitle }}</div>
        <v-divider class="my-4 mx-auto" width="100" color="primary"></v-divider>
      </div>
    </v-col>
  </v-row>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
})
</script>

<style scoped>
.title-wrapper {
  padding-top: 1rem;
}

.title-text {
  position: relative;
  display: inline-block;
}
</style>