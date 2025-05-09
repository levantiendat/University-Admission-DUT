import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import FloatingVue from 'floating-vue'
import 'floating-vue/dist/style.css'

createApp(App).use(store).use(FloatingVue).use(router).mount('#app')
