<template>
  <div>
    <h2>📘 사용자 프로필</h2>
    <p>작성자 ID: {{ userId }}</p>

    <h3>✏️ 작성한 글</h3>
    <ul>
      <li v-for="article in articles" :key="article.id">
        <RouterLink :to="`/community/articles/${article.id}`">{{ article.title }}</RouterLink>
      </li>
    </ul>

    <h3>💬 작성한 댓글</h3>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        {{ comment.content }}
      </li>
    </ul>

    <h3>👥 팔로우 중인 사용자</h3>
    <ul>
      <li v-for="user in followings" :key="user.id">
        <RouterLink :to="`/community/profile/${user.id}`">{{ user.username }}</RouterLink>
      </li>
    </ul>
  </div>
  <h3>👥 팔로워</h3>
<ul>
  <li v-for="user in followers" :key="user.id">
    <RouterLink :to="`/community/profile/${user.id}`">{{ user.username }}</RouterLink>
  </li>
</ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const userId = route.params.id
const articles = ref([])
const comments = ref([])
const followings = ref([])
const followers = ref([])

const fetchFollowers = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/community/users/${userId}/followers/`)
  followers.value = res.data
}

onMounted(async () => {
  await fetchActivity()
  await fetchFollowings()
  await fetchFollowers()   // 추가
})

const fetchActivity = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/community/users/${userId}/activity/`)
  articles.value = res.data.articles
  comments.value = res.data.comments
}

const fetchFollowings = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/community/users/${userId}/followings/`)
  followings.value = res.data
}

onMounted(async () => {
  await fetchActivity()
  await fetchFollowings()
})
</script>
