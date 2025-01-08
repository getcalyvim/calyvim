# WorkspaceLayout.vue
<script setup>
import { Layout, Avatar, Dropdown, Card } from 'ant-design-vue'
import { ref, onMounted } from 'vue'
import {
  LayoutDashboard,
  Kanban,
  Newspaper,
  ListTodo,
  Settings,
  User,
  LogOut,
  Users,
  Building2,
  Bell,
  HelpCircle,
  FileQuestion,
  Github,
  Puzzle,
  Files,
  Calendar,
  List,
  SlidersVertical,
  Grid,
  FileCheck2,
  FileStack,
} from 'lucide-vue-next'

import BaseLayout from '@/components/base/base-layout.vue'
import WorkspaceMenu from '@/components/base/workspace-menu.vue'
import { generateAvatar } from '@/utils/helpers'

const props = defineProps({
  workspace: {
    type: Object,
    required: true,
  },
  page: {
    type: String,
    required: true,
  },
  subPage: {
    type: String,
    default: '',
  },
  dynamicSubmenu: {
    type: Array,
    default: () => [],
  },
  dynamicSubmenuKey: {
    type: String,
    default: '',
  },
})

const collapsed = ref(false)
const openSubmenu = ref('')
const currentUser = ref(null)
const baseMenuItems = ref([
  {
    key: 'dashboard',
    label: 'Dashboard',
    icon: LayoutDashboard,
    redirectPath: `/app/${props.workspace.slug}/`,
  },
  {
    key: 'boards',
    label: 'Boards',
    icon: Grid,
    redirectPath: `/app/${props.workspace.slug}/boards`,
    submenu: [
      {
        key: 'view-all-boards',
        label: 'View all boards',
        icon: List,
        redirectPath: `/app/${props.workspace.slug}/boards`,
      },
    ],
  },
  {
    key: 'documents',
    label: 'Documents',
    icon: FileCheck2,
    redirectPath: `/app/${props.workspace.slug}/documents`,
    submenu: [
      {
        key: 'view-all-documents',
        label: 'View all docs',
        icon: FileStack,
        redirectPath: `/app/${props.workspace.slug}/documents`,
      },
    ],
  },
  {
    key: 'newslines',
    label: 'Newslines',
    icon: Newspaper,
    redirectPath: `/app/${props.workspace.slug}/newslines`,
  },
  {
    key: 'todos',
    label: 'To-dos',
    icon: ListTodo,
    redirectPath: `/app/${props.workspace.slug}/todos`,
  },
  {
    key: 'meetings',
    label: 'Meetings',
    icon: Calendar,
    redirectPath: '/meetings',
    submenu: [
      {
        key: 'view-all-meetings',
        label: 'View all meetings',
        icon: Calendar,
        redirectPath: `/app/${props.workspace.slug}/meetings`,
      },
    ],
  },
  {
    key: 'templates',
    label: 'Templates',
    icon: Files,
    redirectPath: `/app/${props.workspace.slug}/templates`,
  },
  {
    key: 'integrations',
    label: 'Integrations',
    icon: Puzzle,
    redirectPath: `/app/${props.workspace.slug}/integrations`,
  },
  {
    key: 'notifications',
    label: 'Notifications',
    icon: Bell,
    redirectPath: '/notifications',
  },
  {
    key: 'help-support',
    label: 'Help & Support',
    icon: HelpCircle,
    redirectPath: '/help',
    submenu: [
      {
        key: 'contact-support',
        label: 'Contact Support',
        icon: HelpCircle,
        redirectPath: '/help/support',
      },
      {
        key: 'documentation',
        label: 'Documentation',
        icon: Newspaper,
        redirectPath: '/help/docs',
      },
      {
        key: 'faqs',
        label: 'FAQs',
        icon: FileQuestion,
        redirectPath: '/help/faqs',
      },
    ],
  },
  {
    key: 'settings',
    label: 'Settings',
    icon: SlidersVertical,
    redirectPath: '/settings',
    submenu: [
      {
        key: 'general',
        label: 'General',
        icon: Settings,
        redirectPath: `/app/${props.workspace.slug}/settings`,
      },
      {
        key: 'members',
        label: 'Members',
        icon: Users,
        redirectPath: `/app/${props.workspace.slug}/settings/members`,
      },
      {
        key: 'teams',
        label: 'Teams',
        icon: Building2,
        redirectPath: `/app/${props.workspace.slug}/settings/teams`,
      },
      // {
      //   key: 'other',
      //   label: 'Other',
      //   icon: MoreHorizontal,
      //   redirectPath: '/settings/other',
      // },
    ],
  },
])

onMounted(() => {
  // Get current user from localStorage
  const currentUserString = localStorage.getItem('currentUser')
  if (!currentUserString) {
    window.location.href = '/app/accounts/login'
    return
  }
  currentUser.value = JSON.parse(currentUserString)

  // If dynamic submenu is provided, append it to the corresponding menu
  if (props.dynamicSubmenuKey) {
    const baseItem = baseMenuItems.value.find(
      (item) => item.key === props.dynamicSubmenuKey
    )

    if (baseItem) {
      baseItem.submenu = [...(baseItem.submenu || []), ...props.dynamicSubmenu]
      openSubmenu.value = props.dynamicSubmenuKey
    }
  }
})

const toggleSubmenu = (menu) => {
  openSubmenu.value = openSubmenu.value === menu ? '' : menu
}

const isSubmenuOpen = (menu) => openSubmenu.value === menu

const isMenuItemActive = (itemKey) => {
  return props.page === itemKey
}

const handleNavigation = (path) => {
  window.location.href = path
}

const redirectToProfilePage = () => {
  window.location.href = '/app/accounts/profile'
}

const logoutUser = () => {
  localStorage.removeItem('currentUser')
  window.location.href = '/app/accounts/logout'
}

const openWorkspaceMenu = ref(false)
const showWorkspaceMenu = () => {
  openWorkspaceMenu.value = true
}

const openProfileMenu = ref(false)
const showProfileMenu = () => {
  openProfileMenu.value = true
}
</script>

<template>
  <BaseLayout>
    <Layout class="h-screen">
      <Layout.Sider
        v-model:collapsed="collapsed"
        :trigger="null"
        collapsible
        class="h-full border-r-2 border-purple-500 !bg-gray-50"
        theme="light"
      >
        <div class="flex flex-col h-full bg-gray-50">
          <!-- Header section -->
          <div class="p-3 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <Dropdown
                  :trigger="['click']"
                  v-model:open="openWorkspaceMenu"
                  placement="bottomRight"
                >
                  <template #overlay>
                    <WorkspaceMenu :workspace="props.workspace" />
                  </template>
                  <div class="flex items-center gap-1 hover:bg-gray-100 p-1">
                    <Avatar
                      shape="square"
                      :size="24"
                      :src="
                        !!props.workspace.logo
                          ? props.workspace.logoSrc
                          : generateAvatar(props.workspace.name, 10)
                      "
                    />
                    <div class="font-medium text-gray-900 ml-2">
                      {{ props.workspace.name }}
                    </div>
                  </div>
                </Dropdown>
              </div>

              <Dropdown
                :trigger="['click']"
                placement="bottomRight"
                v-model:open="openProfileMenu"
              >
                <Avatar
                  v-if="currentUser"
                  :size="24"
                  :src="
                    currentUser.avatarSrc ||
                    generateAvatar(currentUser.name || 'User', 10)
                  "
                  class="cursor-pointer"
                  shape="square"
                />
                <template #overlay>
                  <Card class="w-72" size="small">
                    <div class="flex flex-col gap-2">
                      <div class="flex flex-col gap-0 mb-2">
                        <div class="font-semibold">
                          {{ currentUser.displayName }}
                        </div>
                        <div class="text-xs">{{ currentUser.email }}</div>
                      </div>
                      <div
                        class="flex items-center gap-1 cursor-pointer"
                        @click="redirectToProfilePage"
                      >
                        <User class="w-4 h-4 text-gray-500" />
                        <div>Accounts</div>
                      </div>
                      <div
                        class="flex items-center gap-1 cursor-pointer"
                        @click="logoutUser"
                      >
                        <LogOut class="w-4 h-4 text-gray-500" />
                        <div>Logout</div>
                      </div>
                    </div>
                  </Card>
                </template>
              </Dropdown>
            </div>
          </div>

          <!-- Menu section -->
          <div class="flex-1 px-2 py-2 bg-gray-50">
            <div v-for="item in baseMenuItems" :key="item.key" class="mb-1">
              <div
                class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer text-gray-600 hover:bg-gray-100 transition-colors"
                :class="{
                  'bg-gray-100 text-primary': item.key === props.page,
                }"
                @click="
                  item.submenu
                    ? toggleSubmenu(item.key)
                    : handleNavigation(item.redirectPath)
                "
              >
                <component
                  :is="item.icon"
                  v-if="item.icon"
                  class="text-gray-500 w-4 h-4"
                  :class="{ 'text-primary': isMenuItemActive(item.key) }"
                />
                <span class="font-medium">{{ item.label }}</span>
                <span
                  v-if="item.submenu"
                  class="ml-auto text-[10px] text-gray-400 transform transition-transform duration-200"
                  :class="{ 'rotate-180': isSubmenuOpen(item.key) }"
                >
                  ▼
                </span>
              </div>

              <div
                v-if="item.submenu"
                class="overflow-hidden transition-all duration-300 ease-in-out"
                :style="{
                  maxHeight: isSubmenuOpen(item.key)
                    ? `${item.submenu.length * 40}px`
                    : '0px',
                  opacity: isSubmenuOpen(item.key) ? 1 : 0,
                }"
              >
                <div
                  v-for="subItem in item.submenu"
                  :key="subItem.key"
                  @click="handleNavigation(subItem.redirectPath)"
                  class="pl-9 pr-3 py-2 text-sm flex flex-col gap-2"
                  :class="{
                    'text-primary bg-gray-50': props.subPage === subItem.key,
                  }"
                >
                  <div
                    v-if="!!subItem?.heading"
                    class="text-xs text-gray-500 font-bold"
                  >
                    {{ subItem.heading }}
                  </div>
                  <div
                    class="flex items-center gap-2 cursor-pointer text-gray-500 hover:text-primary"
                  >
                    <component
                      :is="subItem.icon"
                      class="w-3.5 h-3.5 text-gray-400"
                      :class="{
                        'text-primary': props.subPage === subItem.key,
                      }"
                    />
                    <div
                      :class="{
                        'text-primary': props.subPage === subItem.key,
                      }"
                    >
                      {{ subItem.label }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- GitHub Link Footer -->
          <div class="px-4 py-3 border-t border-gray-200">
            <a
              href="https://github.com/your-repo"
              target="_blank"
              class="flex items-center gap-2 text-gray-400 hover:text-gray-600 transition-colors text-sm"
            >
              <Github class="w-4 h-4" />
              Star us on GitHub
            </a>
          </div>
        </div>
      </Layout.Sider>

      <Layout>
        <Layout.Content class="bg-white">
          <slot></slot>
        </Layout.Content>
      </Layout>
    </Layout>
  </BaseLayout>
</template>
