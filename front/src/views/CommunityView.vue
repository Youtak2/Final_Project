<template>
  <div>
    <h2>📚 게시글 목록</h2>
    <RouterLink to="/community/articles/write">✍️ 글쓰기</RouterLink>
<ul>
  <li v-for="article in articles" :key="article.id">
    <RouterLink :to="`/community/articles/${article.id}`">{{ article.title }}</RouterLink>
    <span>👍 {{ article.liked_users.length }}</span>
    <span v-if="article.liked_users.length >= 30" style="color: red; font-weight: bold;">🔥 핫</span>
  </li>
</ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const articles = ref([])

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/v1/community/articles/')
  articles.value = res.data
})
</script>
