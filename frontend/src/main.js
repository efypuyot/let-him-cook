import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { toast } from 'vue-sonner'

const app = createApp(App)
app.use(router)

// Make toast available globally
app.config.globalProperties.$toast = toast

app.mount('#app')