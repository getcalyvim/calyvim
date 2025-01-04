import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import App from '@/components/boards/settings/labels/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(App, camelcaseKeys(props, { deep: true }))

app.mount('#app')
