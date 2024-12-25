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

const switchTab = (key) => {
  if (key === 'kanban') {
    window.location.href = `/app/b/${props.board.id}/`
  } else {
    window.location.href = `/app/b/${props.board.id}/${key}/`
  }
}
</script>

<template>
  <BaseLayout>
    <Tabs v-model:active-key="activeKey" class="pl-5" @change="switchTab">
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
          <span>
            <AppstoreOutlined />
            Kanban
          </span>
        </template>
      </TabPane>

      <TabPane key="table">
        <template #tab>
          <TableOutlined />
          Table
        </template>
      </TabPane>

      <TabPane key="timeline" disabled>
        <template #tab>
          <CalendarOutlined />
          Timeline
        </template>
      </TabPane>

      <TabPane key="sprints">
        <template #tab>
          <CarryOutOutlined />
          Sprints
        </template>
      </TabPane>

      <TabPane key="settings">
        <template #tab>
          <SettingOutlined />
          Settings
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
