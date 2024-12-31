<script setup>
import { Avatar, Divider, Select, SelectOption, Button } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import { useBoardStore } from '@/stores/board'

import TaskTypeIcon from '../../../icons/task-type-icon.vue'
import {
  ClockCircleOutlined,
  FlagOutlined,
  InboxOutlined,
  SyncOutlined,
} from '@ant-design/icons-vue'
import { h } from 'vue'
import { taskUpdateAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'

const props = defineProps(['task', 'board', 'isArchived', 'groupKey'])
const emit = defineEmits([
  'updateProperties',
  'updateState',
  'updateSprint',
  'archive',
  'log'
])

const store = useBoardStore()

const updateTask = async (taskId, updatedData) => {
  try {
    const { data } = await taskUpdateAPI(props.board.id, taskId, updatedData)
    emit('log', data.log)
    notify('UPDATED', data.log)
  } catch (error) {
    handleResponseError(error)
  }
}

const updatePriority = async (taskId, priorityId) => {
  const priority = store.priorities.find((p) => p.id === priorityId)
  const updatedData = {
    priorityId,
    priority,
  }

  updateTask(taskId, { priorityId })
  store.updateTask(taskId, updatedData, 'priority', priorityId)
}

const updateAssignee = async (taskId, assigneeId) => {
  const assignee = store.members.find((m) => m.id === assigneeId)
  const updatedData = {
    assigneeId,
    assignee,
  }

  updateTask(taskId, { assigneeId })
  store.updateTask(taskId, updatedData, 'assignee', assigneeId)
}

const updateState = async (taskId, stateId) => {
  const state = store.states.find((s) => s.id === stateId)
  const updatedData = {
    stateId,
    state,
  }

  updateTask(taskId, { stateId })
  await store.updateTask(taskId, updatedData, 'state', stateId)
  if(!!props.groupKey) {
    await store.updateTaskPositionByGroup(taskId, stateId, props.groupKey, updatedData)
  } else {
    await store.updateTaskPosition(taskId, stateId, updatedData)
  }
}
</script>

<template>
  <div class="mb-2 font-semibold">State</div>
  <Select
    v-model:value="task.stateId"
    class="w-full mb-2"
    @change="(stateId) => updateState(task.id, stateId)"
  >
    <SelectOption
      :value="state.id"
      v-for="state in store.states"
      :key="state.id"
    >
      <span class="ml-1">{{ state.name }}</span>
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Assignee</div>
  <Select
    v-model:value="task.assigneeId"
    @change="(assigneeId) => updateAssignee(task.id, assigneeId)"
    class="w-full"
  >
    <SelectOption :value="null">None</SelectOption>
    <SelectOption
      :value="member.id"
      v-for="member in store.members"
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
    @change="(taskType) => emit('updateProperties', { taskType })"
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
    @change="(priorityId) => updatePriority(task.id, priorityId)"
    class="w-full"
  >
    <SelectOption :value="null">-</SelectOption>
    <SelectOption
      :value="priority.id"
      v-for="priority in store.priorities"
      :key="priority.id"
    >
      <FlagOutlined />
      <span class="ml-2">{{ priority.name }}</span>
    </SelectOption>
  </Select>

  <template v-if="props.board.isEstimateEnabled">
    <Divider class="p-0 my-3" />

    <div class="mb-2 font-semibold">Estimate</div>
    <Select
      v-model:value="task.estimateId"
      @change="(estimateId) => emit('updateProperties', { estimateId })"
      class="w-full"
    >
      <SelectOption :value="null">-</SelectOption>
      <SelectOption
        :value="estimate.id"
        v-for="estimate in store.estimates"
        :key="estimate.id"
      >
        <ClockCircleOutlined class="text-xs" />
        <span class="ml-1">{{ estimate.value }}</span>
      </SelectOption>
    </Select>
  </template>

  <template v-if="store.sprints.length > 0">
    <Divider class="p-0 my-3" />

    <div class="mb-2 font-semibold">Sprint</div>
    <Select
      v-model:value="task.sprintId"
      @change="(sprintId) => emit('updateSprint', sprintId)"
      class="w-full"
    >
      <SelectOption :value="null">-</SelectOption>
      <SelectOption
        :value="sprint.id"
        v-for="sprint in store.sprints"
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
