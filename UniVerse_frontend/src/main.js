import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
axios.defaults.baseURL='https://fit-akita-deciding.ngrok-free.app/'
axios.defaults.headers.common["ngrok-skip-browser-warning"] = "69420"

app.use(createPinia())
app.use(router,axios)

app.mount('#app')
