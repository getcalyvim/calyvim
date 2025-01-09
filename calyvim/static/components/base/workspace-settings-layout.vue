<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { ref, computed } from 'vue'
import { generateAvatar } from '@/utils/helpers'

const props = defineProps(['workspace', 'currentUser', 'page', 'subPage'])
const activeKey = ref(props.page)

const switchTab = (key) => {
  var redirectUrl = `/${props.workspace.slug}/settings/${key}/`

  if (key === 'general') {
    redirectUrl = `/${props.workspace.slug}/settings/`
  }

  window.location.href = redirectUrl
}

const getWorkspaceLogo = computed(() => {
  if (props.workspace?.logo) {
    return props.workspace.logo
  }

  return generateAvatar(props.workspace.name, 20)
})
</script>

<template>
  <WorkspaceLayout
    :page="props.page"
    :subPage="props.subPage"
    :workspace="props.workspace"
    dynamicSubmenuKey="settings"
  >
    <div class="container mx-auto p-2">
      <div class="text-xl font-semibold mb-2">
        {{ props.workspace.name }}'s settings
      </div>
      
      <slot></slot>
    </div>
  </WorkspaceLayout>
</template>
