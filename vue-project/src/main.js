import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import axios from 'axios';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faCircleCheck, faCircleXmark, faCircle, faSkull, faGavel, faGlobe } from '@fortawesome/free-solid-svg-icons';

/* add icons to the library */
library.add(faCircleCheck, faCircleXmark, faCircle, faSkull, faGavel, faGlobe);

const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8000/api/';
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$TEST_MODE = true;

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia());
app.use(router);

router.isReady().then(() => app.mount('#app'));