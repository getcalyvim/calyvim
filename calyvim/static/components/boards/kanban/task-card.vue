<script setup>
import { Avatar, Tag } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { ClockCircleOutlined, FlagOutlined } from '@ant-design/icons-vue'
import { CalendarClock, Dot } from 'lucide-vue-next'
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

// const store = useBoardStore()
</script>

<template>
  <div class="flex justify-between items-center">
    <div class="text-xs font-semibold mb-1 flex items-center">
      <TaskTypeIcon :taskType="props.task.taskType" />
      <div class="ml-1">{{ props.task.name }}</div>
    </div>

    <div
      v-if="!!props.task.estimate"
      class="flex gap-1"
    >
      <ClockCircleOutlined class="text-xs" />
      <div class="text-xs font-semibold">{{ props.task.estimate?.value }}</div>
    </div>
  </div>

  <div>{{ props.task.summary }}</div>

  <div class="flex gap-3 items-center mt-1 mb-2">
    <div
      v-for="label in props.task.labels"
      :key="label.id"
      class="flex items-center gap-1"
    >
      <div
        class="h-1 w-1 rounded-full"
        :style="{ backgroundColor: label.color }"
      ></div>
      <div class="text-xs leading-none font-semibold">{{ label.name }}</div>
    </div>
  </div>

  <div class="mt-2 flex justify-between items-center">
    <div class="flex items-start gap-1">
      <Tag
        :bordered="false"
        class="text-xs font-semibold"
        v-if="!!props.task.priority"
      >
        <FlagOutlined class="text-primary" />
        <span class="text-primary">{{ props.task?.priority.name }}</span>
      </Tag>

      <Tag
        :bordered="false"
        class="text-xs font-semibold flex items-center gap-1"
        v-if="!!props.task.sprint"
      >
        <CalendarClock class="h-3 w-3" />
        <div>{{ props.task?.sprint.name }}</div>
      </Tag>
    </div>
    <Avatar
      v-if="props.task.assignee"
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
