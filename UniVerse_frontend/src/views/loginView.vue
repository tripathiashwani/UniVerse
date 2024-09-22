<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="main-left">
        <div class="p-8 bg-white border border-gray-200 rounded-lg shadow-sm">
          <h1 class="mb-6 text-2xl font-bold text-gray-800">Log in</h1>

          <p class="mb-6 text-gray-600">
            Welcome back! Log in to access your account and connect with friends. 
            Our secure login process ensures your information stays safe.
          </p>

          <p class="font-medium text-gray-700">
            Don't have an account? <RouterLink :to="{'name': 'signup'}" class="text-purple-600 hover:text-purple-800 underline">Click here</RouterLink> to create one!
          </p>
        </div>
      </div>

      <div class="main-right">
        <div class="p-8 bg-white border border-gray-200 rounded-lg shadow-sm">
          <form class="space-y-6" @submit.prevent="submitForm">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">E-mail</label>
              <input 
                type="email" 
                id="email"
                v-model="form.email" 
                placeholder="Your e-mail address" 
                class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
              >
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input 
                type="password" 
                id="password"
                v-model="form.password" 
                placeholder="Your password" 
                class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
              >
            </div>

            <div v-if="errors.length > 0" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <strong class="font-bold">Error!</strong>
              <ul class="mt-2 list-disc list-inside">
                <li v-for="error in errors" :key="error">{{ error }}</li>
              </ul>
            </div>

            <div>
              <button 
                type="submit"
                class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                Log in
              </button>
              
            </div>
          </form>
          
       
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'


export default {
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const form = ref({
      email: '',
      password: '',
    })
    const errors = ref([])

    const submitForm = async () => {
      errors.value = []

      if (form.value.email === '') {
        errors.value.push('Your e-mail is missing')
      }

      if (form.value.password === '') {
        errors.value.push('Your password is missing')
      }

      if (errors.value.length === 0) {
        try {
          const response = await axios.post('/api/login1/', form.value)
          userStore.setToken(response.data)
          axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access

          const userResponse = await axios.get('/api/me/')
          userStore.setUserInfo(userResponse.data)
          router.push('/feed')
        } catch (error) {
          // console.error('Error during login:', error)
          errors.value.push('The email or password is incorrect! Or the user is not activated!')
        }
      }
    }
    return {
      form,
      errors,
      submitForm,
      userStore,
    }
  }
}
</script>