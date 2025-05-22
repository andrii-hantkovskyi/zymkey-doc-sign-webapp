<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}

const isLoggedIn = computed(() => auth.isAuthenticated)
const isAdmin = computed(() => auth.isAdmin)
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/verify">Verify</RouterLink>
      <RouterLink v-if="isAdmin" to="/sign">Sign</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/register">Register</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/login">Login</RouterLink>
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </nav>
  </header>

  <div class="wrapper">
    <RouterView />
  </div>
</template>

<style scoped>
nav {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  height: 60px;
  background: #42b983;
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}
a, button {
  background: none;
  color: white;
  border: none;
  cursor: pointer;
  font: inherit;
}
button:hover {
  text-decoration: underline;
}
.wrapper {
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  height: calc(100vh - 60px);
}
</style>
