<script setup>
import { Avatar, Divider, Select, SelectOption, Button } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'

import TaskTypeIcon from '../../../icons/task-type-icon.vue'
import {
  ClockCircleOutlined,
  FlagOutlined,
  InboxOutlined,
  SyncOutlined,
} from '@ant-design/icons-vue'
import { h } from 'vue'

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
})

const emit = defineEmits(['update'])
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
      <TaskTypeIcon taskType="issue" />
      <span class="ml-1">Issue</span>
    </SelectOption>
    <SelectOption value="bug">
      <TaskTypeIcon taskType="bug" />
      <span class="ml-1">Bug</span>
    </SelectOption>
    <SelectOption value="story">
      <TaskTypeIcon taskType="story" />
      <span class="ml-1">Story</span>
    </SelectOption>
    <SelectOption value="feature">
      <TaskTypeIcon taskType="feature" />
      <span class="ml-1">Feature</span>
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
      <SelectOption :value="null">-</SelectOption>
      <SelectOption
        :value="sprint.id"
        v-for="sprint in props.sprints"
        :key="sprint.id"
      >
        <SyncOutlined />
        <span class="ml-1">{{ sprint.name }}</span>
      </SelectOption>
    </Select>
  </template>

  <div class="text-base font-semibold mt-4 mb-2">Actions</div>
  <div class="flex flex-col gap-2" v-if="!props.isArchived">
    <Button :icon="h(InboxOutlined)" @click="emit('archive')"
      ><span class="font-semibold">Archive</span></Button
    >
  </div>
</template>

<style scoped></style>
