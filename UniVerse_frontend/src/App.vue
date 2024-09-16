<template>
    <nav class="py-4 px-4 sm:px-8 border-b border-gray-200 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <a href="#" class="text-xl font-bold text-purple-700">Connect!</a>
          </div>
  
          <div class="hidden md:flex items-center justify-center flex-grow">
            <div v-if="userStore.user.isAuthenticated" class="flex space-x-8">
              <RouterLink to="/" class="text-gray-600 hover:text-purple-700">
                <HomeIcon class="w-6 h-6" />
              </RouterLink>
              <RouterLink to="/messages" class="text-gray-600 hover:text-purple-700">
                <MessageSquareIcon class="w-6 h-6" />
              </RouterLink>
              <RouterLink to="/notifications" class="text-gray-600 hover:text-purple-700">
                <BellIcon class="w-6 h-6" />
              </RouterLink>
              <RouterLink to="/search" class="text-gray-600 hover:text-purple-700">
                <SearchIcon class="w-6 h-6" />
              </RouterLink>
            </div>
          </div>
  
          <div class="flex items-center">
            <div v-if="userStore.user.isAuthenticated" class="hidden md:block">
              <RouterLink :to="{ name: 'profile', params: { 'id': userStore.user.id } }">
                <img :src="userStore.user.avatar" class="w-10 h-10 rounded-full" alt="User avatar" />
              </RouterLink>
            </div>
            <div v-else class="hidden md:flex space-x-4">
              <RouterLink to="/login" class="py-2 px-4 bg-gray-600 text-white rounded-lg hover:bg-gray-700">Log in</RouterLink>
              <RouterLink to="/signup" class="py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700">Sign up</RouterLink>
            </div>
            <button @click="toggleMobileMenu" class="md:hidden text-gray-600 hover:text-purple-700 focus:outline-none ml-4">
              <MenuIcon v-if="!isMobileMenuOpen" class="w-6 h-6" />
              <XIcon v-else class="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
  
      <!-- Mobile menu -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-100 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="isMobileMenuOpen" class="md:hidden mt-4 space-y-4">
          <div v-if="userStore.user.isAuthenticated" class="flex flex-col space-y-4">
            <RouterLink to="/" class="text-gray-600 hover:text-purple-700 flex items-center">
              <HomeIcon class="w-6 h-6 mr-2" /> Home
            </RouterLink>
            <RouterLink to="/messages" class="text-gray-600 hover:text-purple-700 flex items-center">
              <MessageSquareIcon class="w-6 h-6 mr-2" /> Messages
            </RouterLink>
            <RouterLink to="/notifications" class="text-gray-600 hover:text-purple-700 flex items-center">
              <BellIcon class="w-6 h-6 mr-2" /> Notifications
            </RouterLink>
            <RouterLink to="/search" class="text-gray-600 hover:text-purple-700 flex items-center">
              <SearchIcon class="w-6 h-6 mr-2" /> Search
            </RouterLink>
            <RouterLink :to="{ name: 'profile', params: { 'id': userStore.user.id } }" class="flex items-center">
              <img :src="userStore.user.avatar" class="w-10 h-10 rounded-full mr-2" alt="User avatar" />
              <span class="text-gray-600">Profile</span>
            </RouterLink>
          </div>
          <div v-else class="flex flex-col space-y-4">
            <RouterLink to="/login" class="py-2 px-4 bg-gray-600 text-white rounded-lg hover:bg-gray-700 text-center">Log in</RouterLink>
            <RouterLink to="/signup" class="py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-center">Sign up</RouterLink>
          </div>
        </div>
      </transition>
    </nav>
  
    <main class="px-4 sm:px-8 py-6 bg-gray-100">
      <RouterView />
    </main>
  
    <button @click="toggleChatbot"
      class="fixed bottom-6 right-6 bg-purple-600 text-white p-3 rounded-full shadow-lg hover:bg-purple-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
      aria-label="Toggle Chatbot">
      <MessageCircleIcon v-if="!isChatbotOpen" class="w-6 h-6" />
      <XIcon v-else class="w-6 h-6" />
    </button>
    <Transition name="slide-fade">
      <div v-if="isChatbotOpen"
        class="fixed bottom-24 right-6 w-full sm:w-96 h-[500px] bg-white rounded-lg shadow-xl overflow-hidden">
        <Chatbot @close="toggleChatbot" />
      </div>
    </Transition>
    <Toast />
  </template>
  
  <script setup>
  import { ref, onBeforeMount } from 'vue'
  import { RouterLink, useRouter } from 'vue-router'
  import axios from 'axios'
  import Toast from '@/components/Toast.vue'
  import { useUserStore } from '@/stores/user'
  import Chatbot from './components/Chatbot.vue'
  import { MessageCircleIcon, XIcon, MenuIcon, HomeIcon, MessageSquareIcon, BellIcon, SearchIcon } from 'lucide-vue-next'
  
  const userStore = useUserStore()
  const isChatbotOpen = ref(false)
  const isMobileMenuOpen = ref(false)
  
  const toggleChatbot = () => {
    isChatbotOpen.value = !isChatbotOpen.value
  }
  
  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  }
  
  onBeforeMount(() => {
    userStore.initStore()
    const token = userStore.user.access
  
    if (token) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token
    } else {
      axios.defaults.headers.common["Authorization"] = ""
    }
  })
  </script>
  
  <style scoped>
  .slide-fade-enter-active,
  .slide-fade-leave-active {
    transition: all 0.3s ease;
  }
  
  .slide-fade-enter-from,
  .slide-fade-leave-to {
    transform: translateY(20px);
    opacity: 0;
  }
  </style>