import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import BoardSettingsPrioritiesApp from '@/components/boards/settings/priorities/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(
    BoardSettingsPrioritiesApp,
  camelcaseKeys(props, { deep: true })
)

app.mount('#app')
