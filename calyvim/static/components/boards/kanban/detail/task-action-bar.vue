<script setup>
import {
  Avatar,
  Divider,
  Select,
  SelectOption,
  Button,
  Tag,
  Badge,
  Dropdown,
  Menu,
  MenuItem,
} from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'

import TaskTypeIcon from '../../../icons/task-type-icon.vue'
import {
  ClockCircleOutlined,
  FlagOutlined,
  InboxOutlined,
  PlusOutlined,
  SyncOutlined,
} from '@ant-design/icons-vue'
import { CalendarClock, CircleDashed, Lock, X } from 'lucide-vue-next'

import { h, computed } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
  board: {
    type: Object,
    required: true,
  },
  isArchived: {
    type: Boolean,
    default: false,
  },
  members: {
    type: Array,
    default: () => [],
  },
  priorities: {
    type: Array,
    default: () => [],
  },
  states: {
    type: Array,
    default: () => [],
  },
  estimates: {
    type: Array,
    default: () => [],
  },
  sprints: {
    type: Array,
    default: () => [],
  },
  labels: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update', 'addLabel', 'deleteLabel'])

const memberIds = computed(() => props.members.map((member) => member.id))
const availableTags = computed(() =>
  props.labels.filter((label) => {
    return !props.task.labels.some((taskLabel) => taskLabel.id === label.id)
  })
)
</script>

<template>
  <div class="mb-2 font-semibold">State</div>
  <Select
    v-model:value="task.stateId"
    class="w-full mb-2"
    @change="(stateId) => emit('update', { stateId })"
  >
    <SelectOption
      :value="state.id"
      v-for="state in props.states"
      :key="state.id"
    >
      <span class="ml-1">{{ state.name }}</span>
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Assignee</div>
  <Select
    v-model:value="task.assigneeId"
    @change="(assigneeId) => emit('update', { assigneeId })"
    class="w-full"
  >
    <SelectOption :value="null">None</SelectOption>
    <SelectOption
      :value="task.assigneeId"
      v-if="!!task.assigneeId && !memberIds.includes(task.assigneeId)"
      disabled
    >
      <Avatar
        :size="22"
        :src="
          !!task?.assignee?.avatar
            ? task.assignee.avatar
            : generateAvatar(task?.assignee?.displayName)
        "
      />
      <span class="ml-2">{{ task?.assignee?.displayName }} </span>
      <Lock class="h-3 w-3 ml-1" />
    </SelectOption>
    <SelectOption
      :value="member.id"
      v-for="member in props.members"
      :key="member.id"
    >
      <Avatar
        :size="22"
        :src="
          !!member.avatar ? member.avatar : generateAvatar(member.displayName)
        "
      />
      <span class="ml-2">{{ member.displayName }}</span>
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Task type</div>
  <Select
    v-model:value="task.taskType"
    class="w-full"
    @change="(taskType) => emit('update', { taskType })"
  >
    <SelectOption value="issue">
      <div class="flex items-center">
        <TaskTypeIcon taskType="issue" />
        <div class="ml-1">Issue</div>
      </div>
    </SelectOption>
    <SelectOption value="bug">
      <div class="flex items-center">
        <TaskTypeIcon taskType="bug" />
        <div class="ml-1">Bug</div>
      </div>
    </SelectOption>
    <SelectOption value="story">
      <div class="flex items-center">
        <TaskTypeIcon taskType="story" />
        <div class="ml-1">Story</div>
      </div>
    </SelectOption>
    <SelectOption value="feature">
      <div class="flex items-center">
        <TaskTypeIcon taskType="feature" />
        <div class="ml-1">Feature</div>
      </div>
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Priority</div>

  <Select
    v-model:value="task.priorityId"
    @change="(priorityId) => emit('update', { priorityId })"
    class="w-full"
  >
    <SelectOption :value="null">None</SelectOption>
    <SelectOption
      :value="priority.id"
      v-for="priority in props.priorities"
      :key="priority.id"
    >
      <FlagOutlined class="text-primary" />
      <span class="ml-2">{{ priority.name }}</span>
    </SelectOption>
  </Select>

  <template v-if="props.board.isEstimateEnabled">
    <Divider class="p-0 my-3" />

    <div class="mb-2 font-semibold">Estimate</div>
    <Select
      v-model:value="task.estimateId"
      @change="(estimateId) => emit('update', { estimateId })"
      class="w-full"
    >
      <SelectOption :value="null">-</SelectOption>
      <SelectOption
        :value="estimate.id"
        v-for="estimate in props.estimates"
        :key="estimate.id"
      >
        <ClockCircleOutlined class="text-xs" />
        <span class="ml-1">{{ estimate.value }}</span>
      </SelectOption>
    </Select>
  </template>

  <template v-if="props.sprints.length > 0">
    <Divider class="p-0 my-3" />

    <div class="mb-2 font-semibold">Sprint</div>
    <Select
      v-model:value="task.sprintId"
      @change="(sprintId) => emit('update', { sprintId })"
      class="w-full"
    >
      <SelectOption :value="null">None</SelectOption>
      <SelectOption
        :value="sprint.id"
        v-for="sprint in props.sprints"
        :key="sprint.id"
      >
        <div class="flex items-center">
          <CalendarClock class="h-3 w-3 text-primary" />
          <div class="ml-1">{{ sprint.name }}</div>
          <CircleDashed
            class="h-3 w-3 text-primary ml-1"
            v-if="sprint.isActive"
          />
        </div>
      </SelectOption>
    </Select>
  </template>

  <Divider class="p-0 my-3" />
  <div class="mb-2 font-semibold flex justify-between items-center">
    <div>Labels</div>
    <Dropdown :trigger="['click']">
      <Button type="text" size="small" :icon="h(PlusOutlined)" />
      <template #overlay>
        <Menu>
          <MenuItem
            v-for="tag in availableTags"
            :key="tag.id"
            @click="emit('addLabel', tag.id)"
          >
            <Badge :color="tag.color" />
            <span>{{ tag.name }}</span>
          </MenuItem>
        </Menu>
      </template>
    </Dropdown>
  </div>
  <div class="flex flex-wrap gap-2 mb-2">
    <Tag
      v-for="label in props.task.labels"
      :key="label.id"
      :bordered="false"
      :color="label.color"
      class="flex items-center"
    >
      <X
        class="h-3 w-3 cursor-pointer"
        @click="emit('deleteLabel', label.id)"
      />
      <div class="ml-2">
        {{ label.name }}
      </div>
    </Tag>
  </div>

  <div class="text-base font-semibold mt-4 mb-2">Actions</div>
  <div class="flex flex-col gap-2" v-if="!props.isArchived">
    <Button :icon="h(InboxOutlined)" @click="emit('archive')">
      <span class="font-semibold">Archive</span>
    </Button>
  </div>
</template>

<style scoped></style>
