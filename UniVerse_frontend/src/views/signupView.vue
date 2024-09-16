<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="main-left">
          <div class="p-8 bg-white border border-gray-200 rounded-lg shadow-sm">
            <h1 class="mb-6 text-3xl font-bold text-gray-800">Sign up</h1>
  
            <p class="mb-6 text-gray-600">
              Join our community today! Create an account to connect with friends,
              share your thoughts, and discover new opportunities. Our simple
              sign-up process ensures you'll be up and running in no time.
            </p>
  
            <p class="font-medium text-gray-700">
              Already have an account? 
              <RouterLink :to="{'name': 'login'}" class="text-purple-600 hover:text-purple-800 underline">
                Click here
              </RouterLink> to log in!
            </p>
          </div>
        </div>
  
        <div class="main-right">
          <div class="p-8 bg-white border border-gray-200 rounded-lg shadow-sm">
            <form class="space-y-6" @submit.prevent="submitForm">
              <div>
                <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                <input 
                  type="text" 
                  id="name"
                  v-model="form.name" 
                  name="name" 
                  placeholder="Your full name" 
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                >
              </div>
  
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700">E-mail</label>
                <input 
                  type="email" 
                  id="email"
                  v-model="form.email" 
                  name="email" 
                  placeholder="Your e-mail address" 
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                >
              </div>
  
              <div>
                <label for="password1" class="block text-sm font-medium text-gray-700">Password</label>
                <input 
                  type="password" 
                  id="password1"
                  v-model="form.password1" 
                  name="password1" 
                  placeholder="Your password" 
                  class="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                >
              </div>
  
              <div>
                <label for="password2" class="block text-sm font-medium text-gray-700">Repeat password</label>
                <input 
                  type="password" 
                  id="password2"
                  v-model="form.password2" 
                  name="password2" 
                  placeholder="Repeat your password" 
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
                  Sign up
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
  import { useToastStore } from '@/stores/toast'
  
  export default {
    setup() {
      const toastStore = useToastStore()
      const router = useRouter()
  
      const form = ref({
        email: '',
        name: '',
        password1: '',
        password2: ''
      })
      const errors = ref([])
  
      const submitForm = async () => {
        errors.value = []
  
        if (form.value.email === '') {
          errors.value.push('Your e-mail is missing')
        }
  
        if (form.value.name === '') {
          errors.value.push('Your name is missing')
        }
  
        if (form.value.password1 === '') {
          errors.value.push('Your password is missing')
        }
  
        if (form.value.password1 !== form.value.password2) {
          errors.value.push('The passwords do not match')
        }
  
        if (errors.value.length === 0) {
          try {
            const response = await axios.post('/api/signup/', form.value)
            console.log(response)
            if (response.data.message === 'success') {
              toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link.', 'bg-emerald-500')
              form.value = {
                email: '',
                name: '',
                password1: '',
                password2: ''
              }
              router.push({ name: 'login' })
            } else {
              const data = JSON.parse(response.data.message)
              for (const key in data) {
                errors.value.push(data[key][0].message)
              }
              toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
            }
          } catch (error) {
            console.error('Error during sign-up:', error)
            toastStore.showToast(5000, 'An error occurred. Please try again later.', 'bg-red-300')
          }
        }
      }
  
      return {
        form,
        errors,
        submitForm,
        toastStore
      }
    }
  }
  </script>