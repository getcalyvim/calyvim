<script setup>
import { Avatar, AvatarGroup, Tag } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import {
  ClockCircleOutlined,
  FlagOutlined,
  MinusCircleOutlined,
  SyncOutlined,
} from '@ant-design/icons-vue'
import { useBoardStore } from '@/stores/board'

// const props = defineProps(['board', 'task'])
const props = defineProps({
  board: {
    type: Object,
    required: true,
  },
  task: {
    type: Object,
    required: true,
  },
  hasCurrentSprint: {
    type: Boolean,
    default: false,
  },
})

const store = useBoardStore()
</script>

<template>
  <div class="flex justify-between items-center">
    <div class="text-xs font-semibold mb-1">
      <TaskTypeIcon :taskType="props.task.taskType" />
      <span class="ml-1">{{ props.task.name }}</span>
    </div>

    <div
      v-if="props.board.isEstimateEnabled && !!props.task.estimate"
      class="flex gap-1"
    >
      <ClockCircleOutlined class="text-xs" />
      <div class="text-xs font-semibold">{{ props.task.estimate?.value }}</div>
    </div>
  </div>

  <div>{{ props.task.summary }}</div>

  <div class="mt-2 flex justify-between items-center">
    <div class="flex items-start gap-1">
      <Tag
        :bordered="false"
        class="text-xs font-semibold"
        v-if="!!props.task.priority && (!store.groupBy || store.groupBy !== 'priority')"
      >
        <FlagOutlined class="text-primary" />
        <span class="text-primary">{{ props.task?.priority.name }}</span>
      </Tag>

      <Tag
        :bordered="false"
        class="text-xs font-semibold"
        v-if="!!props.task.sprint && (!store.groupBy || store.groupBy !== 'sprint')"
      >
        <SyncOutlined />
        <span>{{ props.task?.sprint.name }}</span>
      </Tag>
    </div>
    <Avatar
      v-if="props.task.assignee && (!store.groupBy || store.groupBy !== 'assignee')"
      :size="22"
      class="mr-1"
      :src="
        !!props.task.assignee.avatar
          ? props.task.assignee.avatar
          : generateAvatar(props.task.assignee.displayName)
      "
    />
  </div>
</template>
