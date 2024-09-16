<template>
    <main class="px-4 sm:px-6 lg:px-8 py-6 bg-gray-100">
      <div class="max-w-7xl mx-auto lg:grid lg:grid-cols-4 lg:gap-4">
        <div class="main-center lg:col-span-3 space-y-4">
          <div class="bg-white border border-gray-200 rounded-lg">
            <form @submit.prevent="submitForm" method="post">
              <div class="p-4">  
                <textarea 
                  v-model="body" 
                  class="p-4 w-full bg-gray-100 rounded-lg" 
                  placeholder="What are you thinking about?"
                  rows="3"
                ></textarea>
              </div>
              <div class="p-4 border-t border-gray-100 flex flex-col sm:flex-row justify-between items-center">
                <button 
                  type="button" 
                  class="w-full sm:w-auto mb-2 sm:mb-0 py-2 px-4 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors duration-200"
                >
                  Attach image
                </button>
                <button 
                  type="submit" 
                  class="w-full sm:w-auto py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors duration-200"
                >
                  Post
                </button>
              </div>
            </form>
          </div>
  
          <div 
            v-for="post in posts"
            :key="post.id"
            class="p-4 bg-white border border-gray-200 rounded-lg"
          >
            <FeedItem :post="post" @delete-post="deletePost" />
          </div>
        </div>
  
        <div class="main-right lg:col-span-1 space-y-4 mt-4 lg:mt-0">
          <PeopleYouMayKnow />
          <Trends />
        </div>
      </div>
    </main>
  </template>
  
  <script>
  import axios from 'axios'
  import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
  import Trends from '../components/Trends.vue'
  import FeedItem from '../components/FeedItem.vue'
  
  export default {
    name: 'FeedView',
    components: {
      PeopleYouMayKnow,
      Trends,
      FeedItem,
    },
    data() {
      return {
        posts: [],
        body: '',
      }
    },
    mounted() {
      this.getFeed()
    },
    methods: {
      getFeed() {
        axios
          .get('/api/posts/')
          .then(response => {
            console.log('data', response.data)
            this.posts = response.data
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      deletePost(id) {
        this.posts = this.posts.filter(post => post.id !== id)
      },
      submitForm() {
        axios
          .post('/api/posts/create/', { body: this.body })
          .then(response => {
            console.log('data', response.data)
            this.posts.unshift(response.data)
            this.body = ''
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
  </script>