import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
axios.defaults.baseURL='http://13.60.81.46:80/'

app.use(createPinia())
app.use(router,axios)

app.mount('#app')
