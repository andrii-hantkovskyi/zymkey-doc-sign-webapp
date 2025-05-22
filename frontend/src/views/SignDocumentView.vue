<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/config'

const file = ref(null)
const message = ref('')
const error = ref('')
const auth = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (!auth.isAdmin) {
    router.push('/login')
  }
})

const updateFile = (event) => {
  file.value = event.target.files[0]
}

const signDocument = async () => {
  if (!file.value) {
    error.value = 'Please select a file.'
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', file.value)

    const response = await axios.post(`${API_BASE_URL}/admin/sign_document`, formData, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    })

    const blob = new Blob([response.data], { type: 'application/octet-stream' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${file.value.name}.sig`
    a.click()
    window.URL.revokeObjectURL(url)

    message.value = 'Document signed and downloaded successfully.'
    error.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Signing failed'
    message.value = ''
  }
}
</script>

<template>
  <div>
    <h2>Sign Document</h2>
    <form @submit.prevent="signDocument">
      <input type="file" @change="(e) => updateFile(e)" />
      <button type="submit">Sign</button>
      <p v-if="message" style="color: #42b983">{{ message }}</p>
      <p v-if="error" style="color: red">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
h2 {
  color: #42b983;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 320px;
  margin: 0 auto;
  text-align: center;
}
input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 0.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #36a372;
}
p {
  margin-top: 1rem;
}
</style>
