import './assets/main.css';
import vue3googleLogin from 'vue3-google-login';
import { createApp, provide, h } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import { DefaultApolloClient } from '@vue/apollo-composable';
import apolloClient from './apollo';

axios.defaults.baseURL = 'http://localhost:8000/';
// axios.defaults.baseURL = 'https://fit-akita-deciding.ngrok-free.app/';
// axios.defaults.headers.common["ngrok-skip-browser-warning"] = "true";

// Create Vue app instance
const clientID="97172031860-7uchmbvb0q52fbt0d7u1omjsuuidhip3.apps.googleusercontent.com"
const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },
  render: () => h(App),
});

app.use(vue3googleLogin, { clientId: clientID });


// Use Pinia and router
app.use(createPinia());
app.use(router);
app.use(vue3googleLogin, {
  clientId: clientID,
});
// Mount the app
app.mount('#app');
