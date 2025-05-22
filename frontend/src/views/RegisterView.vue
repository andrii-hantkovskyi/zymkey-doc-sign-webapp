<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { verifyUsername, verifyPassword } from '@/utils'
import { API_BASE_URL } from '@/config'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const router = useRouter()

const register = async () => {
  const username_errors = verifyUsername(username.value)
  const password_errors = verifyPassword(password.value, confirmPassword.value)
  if (username_errors.length > 0) {
    error.value = username_errors[0]
    return
  }
  if (password_errors.length > 0) {
    error.value = password_errors[0]
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  try {
    await axios.post(`${API_BASE_URL}/register`, {
      username: username.value,
      password: password.value,
    })
    error.value = ''
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration failed'
  }
}
</script>

<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
      <button type="submit">Register</button>
      <p v-if="error" style="color: red">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
.register {
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
