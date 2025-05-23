<template>
  <div>
    <h2>✍️ 새 글 작성</h2>
    <input v-model="title" placeholder="제목" />
    <textarea v-model="content" placeholder="내용"></textarea>
    <button @click="submitArticle">작성 완료</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const title = ref('')
const content = ref('')
const router = useRouter()
const token = localStorage.getItem('token')

const submitArticle = async () => {
  await axios.post('http://localhost:8000/api/v1/community/articles/create/', {
    title: title.value,
    content: content.value
  }, {
    headers: {
      Authorization: `Token ${token}`
    }
  })
  router.push('/community/articles')
}
</script>