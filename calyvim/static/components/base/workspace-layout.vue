<script setup>
import { Layout, Menu, Flex, Avatar, Dropdown, Card } from 'ant-design-vue'
import { computed, ref } from 'vue'
import {
  CalendarOutlined,
  DashboardOutlined,
  LogoutOutlined,
  ProfileOutlined,
  ProjectOutlined,
  ReadOutlined,
  SettingOutlined,
} from '@ant-design/icons-vue'

import BaseLayout from '@/components/base/base-layout.vue'
import WorkspaceMenu from '@/components/base/workspace-menu.vue'
import { generateAvatar } from '@/utils/helpers'

const props = defineProps(['workspace', 'page'])

const collapsed = ref(false)
const selectedKeys = ref([props.page])

const changePage = (event) => {
  if (event.key === 'dashboard') {
    window.location.href = `/app/${props.workspace.slug}/`
  } else if (event.key === 'boards') {
    window.location.href = `/app/${props.workspace.slug}/boards`
  } else {
    window.location.href = `/app/${props.workspace.slug}/${event.key}/`
  }
}

const logoutUser = () => {
  window.location.href = '/app/accounts/logout'
}

const redirecToProfilePage = () => {
  window.location.href = '/app/accounts/profile'
}

const openWorkspaceMenu = ref(false)
const showWorkspaceMenu = () => {
  openWorkspaceMenu.value = true
}

const currentUser = computed(() => {
  const currentUserString = localStorage.getItem('currentUser')

  if (!currentUserString) {
    window.location.href = '/app/accounts/login'
  }

  return JSON.parse(currentUserString)
})
</script>

<template>
  <BaseLayout>
    <Layout>
      <Layout.Sider v-model:collapsed="collapsed" :trigger="null" collapsible>
        <div class="p-2">
          <Flex gap="small" justify="space-between" align="center">
            <div>
              <Dropdown
                :trigger="['click']"
                v-model:open="openWorkspaceMenu"
                destroyPopupOnHide
              >
                <div
                  class="flex items-center gap-1 hover:bg-gray-100 cursor-pointer"
                >
                  <Avatar
                    shape="square"
                    :src="
                      !!props.workspace.logo
                        ? props.workspace.logoSrc
                        : generateAvatar(props.workspace.name, 10)
                    "
                  />
                  <div>{{ props.workspace.name }}</div>
                </div>

                <template #overlay>
                  <WorkspaceMenu :workspace="props.workspace" />
                </template>
              </Dropdown>
            </div>
            <Dropdown :trigger="['click']">
              <Avatar
                :src="
                  !!currentUser.avatar
                    ? currentUser.avatarSrc
                    : generateAvatar(currentUser.firstName, 50)
                "
                shape="square"
                size="small"
              />

              <template #overlay>
                <Card size="small" class="w-72">
                  <div class="mb-4">
                    <div class="font-semibold">
                      {{ currentUser.firstName }}
                      {{ currentUser?.lastName }}
                    </div>
                    <div class="text-xs text-gray-600">
                      {{ currentUser.email }}
                    </div>
                  </div>
                  <div
                    class="mt-2 cursor-pointer"
                    @click="redirecToProfilePage"
                  >
                    <ProfileOutlined />
                    <span class="ml-2">View profile</span>
                  </div>
                  <div
                    class="mt-2 cursor-pointer"
                    @click="logoutUser"
                  >
                    <LogoutOutlined />
                    <span class="ml-2">Logout</span>
                  </div>
                </Card>
              </template>
            </Dropdown>
          </Flex>
        </div>
        <Menu v-model:selectedKeys="selectedKeys" mode="inline">
          <Menu.Item key="dashboard">
            <a
              :href="`/app/${props.workspace.slug}/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary':
                  selectedKeys[0] === 'dashboard',
              }"
            >
              <DashboardOutlined />
              <span>Dashboard</span>
            </a>
          </Menu.Item>

          <Menu.Item key="boards">
            <a
              :href="`/app/${props.workspace.slug}/boards`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary': selectedKeys[0] === 'boards',
              }"
            >
              <ProjectOutlined />
              <span>Boards</span>
            </a>
          </Menu.Item>

          <Menu.Item key="newslines">
            <a
              :href="`/app/${props.workspace.slug}/newslines/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary':
                  selectedKeys[0] === 'newslines',
              }"
            >
              <ReadOutlined />
              <span>Newslines</span>
            </a>
          </Menu.Item>

          <Menu.Item key="meetings" disabled>
            <CalendarOutlined />
            <span>Meetings (Coming soon)</span>
          </Menu.Item>

          <Menu.Item key="settings">
            <a
              :href="`/app/${props.workspace.slug}/settings/`"
              class="no-underline text-inherit hover:no-underline hover:text-inherit"
              :class="{
                'text-primary hover:text-primary': selectedKeys[0] === 'boards',
              }"
            >
              <SettingOutlined />
              <span>Settings</span>
            </a>
          </Menu.Item>
        </Menu>
      </Layout.Sider>

      <Layout>
        <Layout.Content>
          <slot></slot>
        </Layout.Content>
      </Layout>
    </Layout>
  </BaseLayout>
</template>

<style scoped>
.workspace-header {
  width: 100%;
  margin-bottom: 10px;
  margin-top: 10px;
}

.ant-layout-sider {
  min-height: 100vh;
  background: #fff;
  border-right: 2px solid #8b5cf6;
}

.ant-layout-content {
  background: #fff;
}

.ant-layout-header {
  background: #fff;
  padding: 0;
  border-bottom: 1px solid gray;
}
</style>
