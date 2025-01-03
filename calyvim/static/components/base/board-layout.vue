<script setup>
import {
  TableOutlined,
  CalendarOutlined,
  CarryOutOutlined,
  SettingOutlined,
  LeftOutlined,
  AppstoreOutlined,
} from '@ant-design/icons-vue'
import { TabPane, Tabs, Avatar } from 'ant-design-vue'
import { ref } from 'vue'
import BaseLayout from '@/components/base/base-layout.vue'
import { generateAvatar } from '@/utils/helpers'

const props = defineProps(['board', 'workspace', 'page'])

const activeKey = ref(props.page)
</script>

<template>
  <BaseLayout>
    <Tabs v-model:active-key="activeKey" class="pl-5">
      <template #leftExtra>
        <div class="flex items-center ml-2 mr-5">
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
          <div class="font-semibold">{{ props.board.name }}</div>
        </div>
      </template>
      <TabPane key="kanban">
        <template #tab>
          <a
            :href="`/app/b/${props.board.id}/`"
            class="no-underline text-inherit hover:no-underline hover:text-inherit"
            :class="{
              'text-primary hover:text-primary': activeKey === 'kanban',
            }"
          >
            <span>
              <AppstoreOutlined />
              Kanban
            </span>
          </a>
        </template>
      </TabPane>

      <!-- <TabPane key="table">
        <template #tab>
          <TableOutlined />
          Table
        </template>
      </TabPane> -->

      <TabPane key="sprints">
        <template #tab>
          <a
            :href="`/app/b/${props.board.id}/sprints/`"
            class="no-underline text-inherit hover:no-underline hover:text-inherit"
            :class="{
              'text-primary hover:text-primary': activeKey === 'sprints',
            }"
          >
            <CarryOutOutlined />
            Sprints
          </a>
        </template>
      </TabPane>

      <TabPane key="timeline" disabled>
        <template #tab>
          <CalendarOutlined />
          Timeline
        </template>
      </TabPane>

      <TabPane key="settings">
        <template #tab>
          <a
            :href="`/app/b/${props.board.id}/settings/`"
            class="no-underline text-inherit hover:no-underline hover:text-inherit"
            :class="{
              'text-primary hover:text-primary': activeKey === 'settings',
            }"
          >
            <SettingOutlined />
            Settings
          </a>
        </template>
      </TabPane>

      <template #rightExtra>
        <slot name="actions"></slot>
      </template>
    </Tabs>
    <div class="pl-5">
      <slot></slot>
    </div>
  </BaseLayout>
</template>
