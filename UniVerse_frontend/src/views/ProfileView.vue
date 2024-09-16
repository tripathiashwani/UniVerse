<template>
    <main class="px-4 sm:px-6 md:px-8 py-6 bg-gray-100 min-h-screen">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="md:col-span-1 space-y-4">
          <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
            <img :src="avatar_" class="w-24 h-24 mx-auto mb-6 rounded-full object-cover" />
  
            <p><strong>{{ user.name }}</strong></p>
            <div class="mt-6 space-y-2">
              <button
                class="w-full py-2 px-3 bg-purple-600 text-xs text-white rounded-lg hover:bg-purple-700 transition duration-300"
                @click="sendFriendshipRequest"
                v-if="userStore.user.id !== user.id && can_send_friendship_request"
              >
                Send friendship request
              </button>
              <button
                class="w-full py-2 px-3 bg-purple-600 text-xs text-white rounded-lg hover:bg-purple-700 transition duration-300"
                @click="goToChatRoom"
                v-if="userStore.user.id !== user.id"
              >
                Message
              </button>
            </div>
            <div v-if="user.id === userStore.user.id" class="mt-6">
              <input type="file" @change="handleAvatarChange" class="hidden" id="avatar-upload" ref="avatarInput">
              <label
                for="avatar-upload"
                class="inline-block w-full py-2 px-3 bg-gray-200 text-xs text-gray-700 rounded-lg cursor-pointer hover:bg-gray-300 transition duration-300"
              >
                Choose Avatar
              </label>
              <button
                class="w-full py-2 px-3 bg-purple-600 text-xs text-white rounded-lg mt-2 hover:bg-purple-700 transition duration-300"
                @click="uploadAvatar"
              >
                Update Avatar
              </button>
            </div>
  
            <div class="mt-6 flex space-x-8 justify-around">
              <p class="text-xs text-gray-500">182 friends</p>
              <p class="text-xs text-gray-500">120 posts</p>
            </div>
          </div>
          <div class="space-y-4 hidden md:block">
            <PeopleYouMayKnow />
            <trends />
          </div>
        </div>
  
        <div class="md:col-span-3 space-y-4">
          <div class="bg-white border border-gray-200 rounded-lg" v-if="user.id === userStore.user.id">
            <form @submit.prevent="submitform" method="post">
              <div class="p-4">
                <textarea
                  v-model="body"
                  class="p-4 w-full bg-gray-100 rounded-lg resize-none"
                  placeholder="What are you thinking about?"
                  rows="3"
                ></textarea>
              </div>
  
              <div class="p-4 border-t border-gray-100 flex flex-col sm:flex-row justify-between space-y-2 sm:space-y-0">
                <button type="button" class="w-full sm:w-auto py-2 px-4 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition duration-300">
                  Attach image
                </button>
                <button type="submit" class="w-full sm:w-auto py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition duration-300">
                  Post
                </button>
              </div>
            </form>
          </div>
  
          <div v-for="post in posts" :key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
            <FeedItem :post="post" />
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <script>
  import axios from 'axios'
  import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
  import Trends from '../components/Trends.vue'
  import FeedItem from '../components/FeedItem.vue'
  import { useUserStore } from '@/stores/user'
  import { useToastStore } from '@/stores/toast'
  
  export default {
    name: 'ProfileView',
    components: {
      PeopleYouMayKnow,
      Trends,
      FeedItem,
    },
    setup() {
      const userStore = useUserStore()
      const toastStore = useToastStore()
      return {
        userStore,
        toastStore
      }
    },
    data() {
      return {
        posts: [],
        body: '',
        user: {},
        can_send_friendship_request: null,
        selectedFile: null,
        avatar_: ''
      }
    },
    mounted() {
      this.getFeed()
    },
    watch: {
      '$route.params.id': {
        handler: function () {
          this.getFeed()
        },
        deep: true,
        immediate: true
      }
    },
    methods: {
      handleAvatarChange(event) {
        const file = event.target.files[0]
        if (file) {
          this.selectedFile = file
        }
      },
      async uploadAvatar() {
        if (this.selectedFile) {
          const formData = new FormData()
          formData.append('avatar', this.selectedFile)
  
          try {
            const response = await axios.put('/api/profile_picture/', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
            this.userStore.setUserInfo(response.data)
            this.avatar_ = this.userStore.user.avatar
            this.toastStore.showToast(5000, 'Avatar updated successfully!', 'bg-emerald-300')
          } catch (error) {
            console.log('error', error)
            this.toastStore.showToast(5000, 'Failed to update avatar.', 'bg-red-300')
          }
        }
      },
      sendFriendshipRequest() {
        axios
          .post(`/api/friends/${this.$route.params.id}/request/`)
          .then(response => {
            this.can_send_friendship_request = false
            if (response.data.message == 'request already sent') {
              this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
            } else {
              this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
            }
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      getFeed() {
        axios
          .get(`/api/posts/profile/${this.$route.params.id}/`)
          .then(response => {
            this.posts = response.data.posts
            this.user = response.data.user
            this.can_send_friendship_request = response.data.can_send_friendship_request
            this.avatar_ = "https://fit-akita-deciding.ngrok-free.app/api" + response.data.user.avatar
            // this.avatar_ = "http://localhost:8000/api" + response.data.user.avatar
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      goToChatRoom() {
        const currentUserID = this.userStore.user.id
        const profileUserID = this.$route.params.id
        const roomID = currentUserID < profileUserID ? `${currentUserID}_${profileUserID}` : `${profileUserID}_${currentUserID}`
        this.$router.push({ name: 'ChatRoom', params: { roomID } })
      },
      submitform() {
        axios
          .post('/api/posts/create/', { 'body': this.body })
          .then(response => {
            this.posts.unshift(response.data)
            this.body = ''
          })
          .catch(error => {
            console.log('error', error)
          })
      },
    }
  }
  </script>