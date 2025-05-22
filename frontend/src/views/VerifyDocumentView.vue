<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/config'

const file = ref(null)
const signatureFile = ref(null)
const result = ref('')
const error = ref('')

const updateFile = (event, isSignature = false) => {
  if (isSignature) {
    signatureFile.value = event.target.files[0]
  } else {
    file.value = event.target.files[0]
  }
}

const verifyDocument = async () => {
  if (!file.value || !signatureFile.value) {
    error.value = 'Please select both document and signature files.'
    result.value = ''
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('signature_file', signatureFile.value)

    const response = await axios.post(`${API_BASE_URL}/verify_sign`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    result.value = response.data.valid ? '✅ Signature is valid.' : '❌ Signature is NOT valid.'
    error.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Verification failed.'
    result.value = ''
  }
}
</script>

<template>
  <div>
    <h2>Verify Signature</h2>
    <form @submit.prevent="verifyDocument">
      <label for="file">Document File:</label>
      <input type="file" @change="(e) => updateFile(e)" />
      <label for="signature_file">Signature File:</label>
      <input type="file" @change="(e) => updateFile(e, true)" />
      <button type="submit">Verify</button>
      <p v-if="result" :style="{ color: result.includes('✅') ? '#42b983' : 'red' }">
        {{ result }}
      </p>
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
