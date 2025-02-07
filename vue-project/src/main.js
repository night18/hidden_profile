import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import axios from 'axios';



const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8000/api/';
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$TEST_MODE = true;

app.use(createPinia());
app.use(router);

router.isReady().then(() => app.mount('#app'));