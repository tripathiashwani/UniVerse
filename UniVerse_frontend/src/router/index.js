import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import signupView from '../views/signupView.vue'
import loginView from '../views/loginView.vue'
import feedView from '../views/feedView.vue'
import MessagesView from '../views/MessagesView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: signupView
    },
    {
      path: '/login',
      name: 'login',
      component: loginView
    },
    {
      path: '/feed',
      name: 'feed',
      component: feedView
    },
    {
      path: '/messages',
      name: 'messages',
      component: MessagesView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
