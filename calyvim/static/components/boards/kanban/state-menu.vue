<script setup>
import { Menu, MenuItem, SubMenu } from 'ant-design-vue'
import { ref } from 'vue'
import { taskBulkStateUpdateAPI, taskBulkUpdateAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'
import {
  BetweenHorizontalStart,
  ArrowRightLeft,
  Package2,
} from 'lucide-vue-next'

import { useBoardStore } from '@/stores/board'

const props = defineProps(['state', 'board'])

const store = useBoardStore()

const getTaskIds = (prevStateId) => {
  if (!!store.groupBy) {
    return store.kanban
      .map((group) => group.states)
      .flat()
      .filter((state) => state.id === prevStateId)
      .map((state) => state.tasks)
      .flat()
      .map((task) => task.id)
  } else {
    return store.kanban
      .map((state) => state.tasks)
      .flat()
      .filter((task) => task.stateId === prevStateId)
      .map((task) => task.id)
  }
}

const bulkTaskUpdate = async (property, value) => {
  const taskIds = getTaskIds(props.state.id)
  const updateData = {
    ids: taskIds,
    property: property,
    value: value,
  }

  try {
    const { data } = await taskBulkUpdateAPI(props.board.id, updateData)
    // TODO: Update the board with the new updated tasks and their layour

    notify('UPDATED', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <Menu>
    <SubMenu>
      <template #title>
        <BetweenHorizontalStart class="w-4 h-4 align-middle" />
        <span class="ml-2">Move all tasks to another state</span>
      </template>

      <MenuItem
        v-for="state in store.states"
        :key="state.id"
        :disabled="state.id === props.state.id"
        @click="bulkTaskUpdate('state', state.id)"
      >
        {{ state.name }}
      </MenuItem>
    </SubMenu>
    <SubMenu>
      <template #title>
        <ArrowRightLeft class="w-4 h-4 align-middle" />
        <span class="ml-2">Transfer tasks to another sprint</span>
      </template>
      <div class="h-64 overflow-y-auto">
        <MenuItem
          v-for="sprint in store.sprints"
          :key="sprint.id"
          @click="bulkTaskUpdate('sprint', sprint.id)"
        >
          {{ sprint.name }}
        </MenuItem>
      </div>
    </SubMenu>
    <MenuItem>
      <Package2 class="w-4 h-4 align-middle" />
      <span class="ml-2">Archive all tasks in the {{ props.state.name }}</span>
    </MenuItem>
  </Menu>
</template>
