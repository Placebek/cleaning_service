import { createApp } from 'vue'
import App from './App.vue'
import '../src/assets/base.css'
import { createPinia } from 'pinia'
import { router } from './router/auth'
import PrimeVue from 'primevue/config'
import Clipboard from 'v-clipboard'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Clipboard)
app.use(PrimeVue, {
	theme: 'none',
})
app.mount('#app')

// app.use(createPinia())
