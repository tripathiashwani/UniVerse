<template>
    <main class="px-4 sm:px-6 lg:px-8 py-6 bg-gray-100">
      <div class="max-w-7xl mx-auto lg:grid lg:grid-cols-4 lg:gap-8">
        <div class="lg:col-span-3 space-y-6">
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <form @submit.prevent="submitForm" class="p-4 flex space-x-2">  
              <input 
                v-model="query" 
                type="search" 
                class="flex-grow p-2 bg-gray-100 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent" 
                placeholder="What are you looking for?"
              >
              <button class="p-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition duration-150 ease-in-out">
                <SearchIcon class="w-6 h-6" />
              </button>
            </form>
          </div>
  
          <div v-if="users.length > 0" class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <h2 class="text-xl font-semibold p-4 border-b border-gray-200">Users</h2>
            <div class="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              <div 
                v-for="user in users"
                :key="user.id"
                class="p-4 text-center bg-gray-50 rounded-lg hover:bg-gray-100 transition duration-150 ease-in-out"
              >
                <RouterLink :to="{name: 'profile', params:{'id': user.id}}" class="block">
                  <img :src="getAvatarUrl(user.avatar)" :alt="user.name" class="w-20 h-20 rounded-full mx-auto mb-3 object-cover">
                  <p class="font-medium text-gray-900">{{ user.name }}</p>
                </RouterLink>
                <div class="mt-3 flex justify-around text-xs text-gray-500">
                  <p>182 friends</p>
                  <p>120 posts</p>
                </div>
              </div>
            </div>
          </div>
  
          <div v-if="posts.length > 0" class="space-y-6">
            <h2 class="text-xl font-semibold">Posts</h2>
            <div 
              v-for="post in posts"
              :key="post.id"
              class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden"
            >
              <FeedItem :post="post" />
            </div>
          </div>
  
          <div v-if="users.length === 0 && posts.length === 0 && query" class="text-center py-12 bg-white rounded-lg shadow-sm">
            <SearchXIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No results found</h3>
            <p class="mt-1 text-sm text-gray-500">We couldn't find anything matching your search. Try different keywords.</p>
          </div>
        </div>
  
        <div class="hidden lg:block space-y-6">
          <PeopleYouMayKnow />
          <Trends />
        </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
  import Trends from '../components/Trends.vue'
  import FeedItem from '../components/FeedItem.vue'
  import { SearchIcon, SearchXIcon } from 'lucide-vue-next'
  
  const router = useRouter()
  
  const query = ref('')
  const users = ref([])
  const posts = ref([])
  
  const submitForm = async () => {
    try {
      const response = await axios.post('/api/search/', { query: query.value })
      localStorage.setItem('queryold', query.value)
      users.value = response.data.users
      posts.value = response.data.posts
    } catch (error) {
      console.error('Error during search:', error)
    }
  }
  
  const getAvatarUrl = (avatar) => {
    return `https://fit-akita-deciding.ngrok-free.app/api${avatar}`
  }
  
  onMounted(() => {
    query.value = localStorage.getItem('queryold') || ''
    if (query.value) {
      submitForm()
    }
  })
  </script>