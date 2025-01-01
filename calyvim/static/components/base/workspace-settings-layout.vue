<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import {
  ApiOutlined,
  CreditCardOutlined,
  ExportOutlined,
  ProfileOutlined,
  TeamOutlined,
  UserOutlined,
} from '@ant-design/icons-vue'
import { Avatar, TabPane, Tabs } from 'ant-design-vue'
import { ref, computed } from 'vue'
import { generateAvatar } from '@/utils/helpers'

const props = defineProps(['workspace', 'currentUser', 'page'])
const activeKey = ref(props.page)

const switchTab = (key) => {
  var redirectUrl = `/app/${props.workspace.slug}/settings/${key}/`

  if (key === 'general') {
    redirectUrl = `/app/${props.workspace.slug}/settings/`
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
    page="settings"
    :workspace="props.workspace"
    :currentUser="props.currentUser"
  >
    <div class="container mx-auto p-2">
      <div class="text-xl font-semibold mb-2">
        {{ props.workspace.name }}'s settings
      </div>
      <Tabs v-model:activeKey="activeKey">
        <TabPane key="general">
          <template #tab>
            <a
              :href="`/app/${props.workspace.slug}/settings/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary': activeKey === 'general',
              }"
            >
              <ProfileOutlined />
              <span>General</span>
            </a>
          </template>
        </TabPane>

        <TabPane key="members">
          <template #tab>
            <a
              :href="`/app/${props.workspace.slug}/settings/members/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary': activeKey === 'members',
              }"
            >
              <UserOutlined />
              <span>Members</span>
            </a>
          </template>
        </TabPane>

        <TabPane key="teams">
          <template #tab>
            <a
              :href="`/app/${props.workspace.slug}/settings/teams/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary': activeKey === 'teams',
              }"
            >
              <TeamOutlined />
              <span>Teams</span>
            </a>
          </template>
        </TabPane>

        <TabPane key="integrations" disabled>
          <template #tab>
            <ApiOutlined />
            <span>Integrations</span>
          </template>
        </TabPane>

        <TabPane key="billing" disabled>
          <template #tab>
            <CreditCardOutlined />
            <span>Billing</span>
          </template>
        </TabPane>

        <TabPane key="exports" disabled>
          <template #tab>
            <ExportOutlined />
            <span>Exports</span>
          </template>
        </TabPane>
      </Tabs>
      <slot></slot>
    </div>
  </WorkspaceLayout>
</template>
