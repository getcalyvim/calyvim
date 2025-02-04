<script setup>
import { Avatar, Tag } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { ClockCircleOutlined, FlagOutlined } from '@ant-design/icons-vue'
import { CalendarClock, Dot, CalendarRange } from 'lucide-vue-next'
import { useBoardStore } from '@/stores/board'
import { PhCalendar, PhCalendarBlank, PhPersonSimpleRun } from '@phosphor-icons/vue'

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
  <div class="flex justify-between items-center mb-1">
    <div class="text-xs font-semibold mb-1 flex items-center">
      <TaskTypeIcon :taskType="props.task.taskType" />
      <div class="ml-1">{{ props.task.name }}</div>
    </div>

    <Tag
      :bordered="false"
      class="text-xs font-semibold me-0"
      v-if="!!props.task.priority"
    >
      <FlagOutlined class="text-primary" />
      <span class="text-primary">{{ props.task?.priority.name }}</span>
    </Tag>
  </div>

  <div>{{ props.task.summary }}</div>

  <div class="flex gap-0.2 items-center mt-1 mb-2">
    <Tag
      v-for="label in props.task.labels"
      :key="label.id"
      class="flex items-center gap-1 rounded-full border py-0.5"
      :style="{ borderColor: label.color }"
    >
      <div class="text-xs leading-none font-semibold">{{ label.name }}</div>
    </Tag>
  </div>

  <div class="mt-2 flex justify-between items-center">
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
    <Tag
      :bordered="false"
      class="text-xs font-semibold flex items-center gap-1"
      v-if="!!props.task.sprint"
    >
      <PhPersonSimpleRun weight="bold" />
      <div>{{ props.task?.sprint.name }}</div>
    </Tag>
    <div v-if="!!props.task.estimate" class="flex gap-1 items-center">
      <PhCalendarBlank weight="bold" />
      <div class="text-xs font-semibold">
        {{ props.task.estimate?.value }}
      </div>
    </div>
  </div>
</template>
