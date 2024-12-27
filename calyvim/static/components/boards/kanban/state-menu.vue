<script setup>
import { DoubleRightOutlined, FolderOpenOutlined } from '@ant-design/icons-vue'
import { Menu, MenuItem, SubMenu } from 'ant-design-vue'
import { ref } from 'vue'
import { taskBulkStateUpdateAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'

import { useKanbanStore } from '@/stores/kanban'

const props = defineProps(['state', 'board'])

const store = useKanbanStore()

const bulkStateUpdate = async (stateId) => {
  const state = store.kanban.find((s) => s.id === props.state.id)
  const taskIds = state.tasks.map((task) => task.id)
  try {
    const { data } = await taskBulkStateUpdateAPI(
      props.board.id,
      stateId,
      taskIds
    )
    const newState = store.kanban.find((s) => s.id === stateId)
    state.tasks = state.tasks.filter((task) => !taskIds.includes(task.id))
    newState.tasks.push(...data.tasks)
    notify('MOVED', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <Menu>
    <SubMenu>
      <template #title>
        <DoubleRightOutlined />
        <span class="ml-2">Move all tasks to another state</span>
      </template>

      <MenuItem
        v-for="state in store.states"
        :key="state.id"
        :disabled="state.id === props.state.id"
        @click="bulkStateUpdate(state.id)"
      >
        {{ state.name }}
      </MenuItem>
    </SubMenu>
    <MenuItem>
      <FolderOpenOutlined />
      <span class="ml-2">Archive all tasks in the {{ props.state.name }}</span>
    </MenuItem>
  </Menu>
</template>
