<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
import { useAuthStore } from '@/stores/auth'
import { API_BASE_URL } from '@/config'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const login = async () => {
  try {
    const form = new URLSearchParams()
    form.append('username', username.value)
    form.append('password', password.value)

    const res = await axios.post(`${API_BASE_URL}/token`, form)

    const token = res.data.access_token
    const decoded = jwtDecode(token)

    auth.setToken(token)
    auth.setUsername(decoded.sub)
    auth.setIsAdmin(decoded.is_admin)

    router.push('/verify')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed'
  }
}
</script>

<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p v-if="error" style="color: red">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 320px;
  text-align: center;
}
h2 {
  color: #42b983;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
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
