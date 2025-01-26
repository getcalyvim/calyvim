<script setup>
import { Tabs, Avatar } from 'ant-design-vue'
import { ref, h } from 'vue'
import WorkspaceLayout from './workspace-layout.vue'
import { generateAvatar } from '@/utils/helpers'
import { CalendarClock, Settings2, FastForward, Grid } from 'lucide-vue-next'
const props = defineProps([
  'board',
  'workspace',
  'page',
  'subPage',
  'currentSprint',
])

const activeKey = ref(props.page)

const subMenuItems = [
  {
    heading: `${props.board.name}`,
    label: 'Board Tasks',
    icon: Grid,
    key: 'tasks',
    redirectPath: `/boards/${props.board.id}/tasks/`,
  },
  {
    label: 'Active Sprints',
    icon: CalendarClock,
    key: 'sprints',
    redirectPath: `/boards/${props.board.id}/sprints/`,
  },
  {
    label: 'Settings',
    icon: Settings2,
    key: 'settings',
    redirectPath: `/boards/${props.board.id}/settings/`,
  },
]
</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :page="props.page"
    :dynamicSubmenu="subMenuItems"
    dynamicSubmenuKey="boards"
    :subPage="props.subPage"
  >
    <Tabs v-model:active-key="activeKey" class="pl-1">
      <template #leftExtra>
        <div class="flex items-center ml-2 mr-5 my-3 gap-1">
          <Avatar
            size="small"
            class="mr-2"
            shape="square"
            :src="
              !!props.board.logo
                ? props.board.logo
                : generateAvatar(props.board.name, 10)
            "
          />
          <div class="font-bold">{{ props.board.name }}</div>
          <div v-if="!!props.currentSprint" class="ml-2 flex items-center gap-1">
            <FastForward class="h-4 w-4 text-primary mr-1" />
            <div class="text-xs font-semibold">{{ props.currentSprint.name }}</div>
          </div>
        </div>
      </template>

      <template #rightExtra>
        <slot name="actions"></slot>
      </template>
    </Tabs>
    <div class="pl-2">
      <slot></slot>
    </div>
  </WorkspaceLayout>
</template>
