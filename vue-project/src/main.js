import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import axios from 'axios';
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faCircleCheck, faCircleXmark, faCircle, faSkull, faGavel, faGlobe, faUser, faRobot } from '@fortawesome/free-solid-svg-icons';

/* add icons to the library */
library.add(faCircleCheck, faCircleXmark, faCircle, faSkull, faGavel, faGlobe, faUser, faRobot);

const app = createApp(App);

axios.defaults.baseURL = import.meta.env.VITE_API_URL;
app.config.globalProperties.$axios = axios;

/* The switch to test mode is done here
 * This is a global variable that can be accessed from any component
 * This is useful for testing purposes */
app.config.globalProperties.$TEST_MODE = import.meta.env.VITE_TEST_MODE === 'true';

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia());
app.use(VueSweetalert2);
app.use(router);

router.isReady().then(() => app.mount('#app'));