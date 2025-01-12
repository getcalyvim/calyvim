<script setup>
import { Tabs, Avatar } from 'ant-design-vue'
import { ref, h } from 'vue'
import WorkspaceLayout from './workspace-layout.vue'
import { generateAvatar } from '@/utils/helpers'
import {
  Kanban,
  CalendarClock,
  Settings2,
  BookOpen,
  ImageDown
} from 'lucide-vue-next'
const props = defineProps(['document', 'workspace', 'page', 'subPage'])

const activeKey = ref(props.page)

const subMenuItems = [
  {
    heading: `${props.document.name}`,
    label: 'Page',
    icon: BookOpen,
    key: 'page',
    redirectPath: `/documents/${props.document.id}`
  },
  {
    label: 'Media',
    icon: ImageDown,
    key: 'media',
    redirectPath: `/boards/${props.document.id}/media`
  },
   
//   {
//     label: 'Settings',
//     icon: Settings2,
//     key: 'settings',
//     redirectPath: `/boards/${props.board.id}/settings`
//   }
]
</script>

<template>
  <WorkspaceLayout :workspace="props.workspace" :page="props.page" :dynamicSubmenu="subMenuItems" dynamicSubmenuKey="documents" :subPage="props.subPage">
    <div class="pl-2">
      <slot></slot>
    </div>
  </WorkspaceLayout>
</template>
