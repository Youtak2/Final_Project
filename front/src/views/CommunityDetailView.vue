<template>
  <div>
    <h2>{{ article.title }}</h2>

    <p v-if="article.user">
      ✏️ 작성자:
      <RouterLink :to="`/community/profile/${article.user.id}`">{{ article.user.username }}</RouterLink>
      <button
        v-if="token && article.user?.id !== myId"
        @click="toggleFollow(article.user?.id)"
      >
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button>
    </p>

    <p>{{ article.content }}</p>

    <button v-if="token" @click="toggleLike">
      ❤️ 좋아요 ({{ article.liked_users?.length || 0 }})
    </button>

    <h3>💬 댓글</h3>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        🗣 {{ comment.user.username }}: {{ comment.content }}
        <button @click="setReplyTarget(comment.id)">답글</button>

        <!-- 대댓글 -->
        <ul v-if="comment.replies && comment.replies.length" style="margin-left: 1em;">
          <li v-for="reply in comment.replies" :key="reply.id">
            ↪️ {{ reply.user.username }}: {{ reply.content }}

            <!-- 대댓글에는 답글 버튼 없음 -->
            <div v-if="replyTarget === reply.id && token" style="margin-left: 1em;">
              <textarea v-model="newReply" placeholder="답글을 입력하세요..."></textarea>
              <button @click="submitReply(reply.id)">등록</button>
            </div>
          </li>
        </ul>

        <!-- 댓글에 대한 대댓글 입력창 -->
        <div v-if="replyTarget === comment.id && token">
          <textarea v-model="newReply" placeholder="대댓글 입력..."></textarea>
          <button @click="submitReply(comment.id)">등록</button>
        </div>
      </li>
    </ul>

    <div v-if="token">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요..."></textarea>
      <button @click="submitComment">댓글 작성</button>
    </div>
    <div v-else>
      <p>댓글을 작성하려면 로그인하세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const article = ref({})
const comments = ref([])
const newComment = ref('')
const replyTarget = ref(null)
const newReply = ref('')
const token = localStorage.getItem('token')
const myId = ref(null)
const isFollowing = ref(false)

onMounted(async () => {
  if (token) {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/auth/user/', {
        headers: { Authorization: `Token ${token}` }
      })
      myId.value = res.data.id
    } catch (e) {
      console.error('내 정보 가져오기 실패:', e)
    }
  }

  await fetchArticle()
  await fetchComments()
})

const fetchArticle = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/community/articles/${route.params.id}/`, {
    headers: token ? { Authorization: `Token ${token}` } : {}
  })
  article.value = res.data
  isFollowing.value = res.data.is_following // ✅ 서버 응답에서 상태 반영
}

const fetchComments = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/community/articles/${route.params.id}/comments/`)
  comments.value = res.data
}

const submitComment = async () => {
  if (!newComment.value) return
  await axios.post(`http://localhost:8000/api/v1/community/articles/${route.params.id}/comments/create/`, {
    content: newComment.value
  }, {
    headers: { Authorization: `Token ${token}` }
  })
  newComment.value = ''
  await fetchComments()
}

const setReplyTarget = (commentId) => {
  replyTarget.value = commentId
  newReply.value = ''
}

const submitReply = async (parentId) => {
  if (!newReply.value) return
  replyTarget.value = null
  const content = newReply.value
  newReply.value = ''

  await axios.post(`http://localhost:8000/api/v1/community/articles/${route.params.id}/comments/create/`, {
    content,
    parent: parentId
  }, {
    headers: { Authorization: `Token ${token}` }
  })
  await fetchComments()
}

const toggleLike = async () => {
  await axios.post(`http://localhost:8000/api/v1/community/articles/${route.params.id}/like/`, {}, {
    headers: { Authorization: `Token ${token}` }
  })
  await fetchArticle()
}

const toggleFollow = async (userId) => {
  if (!userId || userId === myId.value) {
    alert('본인은 팔로우할 수 없습니다.')
    return
  }

  try {
    await axios.post(`http://localhost:8000/api/v1/community/users/${userId}/follow/`, {}, {
      headers: { Authorization: `Token ${token}` }
    })
    isFollowing.value = !isFollowing.value
  } catch (e) {
    console.error('팔로우 실패:', e)
    alert(e.response?.data?.detail || '팔로우 처리 중 오류가 발생했습니다.')
  }
}
</script>
