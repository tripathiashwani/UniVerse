import './assets/main.css';

import { createApp, provide, h } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import { DefaultApolloClient } from '@vue/apollo-composable';
import apolloClient from './apollo';

// Configure Axios
axios.defaults.baseURL = 'http://localhost:8000/';
// axios.defaults.baseURL = 'https://fit-akita-deciding.ngrok-free.app/';
axios.defaults.headers.common["ngrok-skip-browser-warning"] = "true";

// Create Vue app instance
const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },
  render: () => h(App),
});

// Use Pinia and router
app.use(createPinia());
app.use(router);

// Mount the app
app.mount('#app');
