<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue'
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { h, onMounted, ref } from 'vue'
import { useNProgress } from '@vueuse/integrations/useNProgress'

import { priorityListAPI, priorityUpdateAPI, priorityDeleteAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'
import { List, ListItem, Button, Divider, Dropdown } from 'ant-design-vue'
import {
  CloseOutlined,
  EditOutlined,
  FlagOutlined,
} from '@ant-design/icons-vue'
import PriorityEdit from './priority-edit.vue'
import PriorityAdd from './priority-add.vue'

const props = defineProps(['workspace', 'board', 'hasEditPermission'])

const priorities = ref([])
const { isLoading } = useNProgress(null, { minimum: '0.5' })

const fetchPriorities = async () => {
  try {
    isLoading.value = true
    const { data } = await priorityListAPI(props.board.id)
    priorities.value = data
  } catch (error) {
    handleResponseError(error)
  } finally {
    isLoading.value = false
  }
}

const selectedPriority = ref(null)
const openPriorityEditForm = (priorityId) => {
  selectedPriority.value = priorityId
}
const closeEditForm = () => {
  selectedPriority.value = null
}
const updatePriority = async (priorityId, values) => {
  try {
    const priority = priorities.value.find((p) => p.id === priorityId)
    const { data } = await priorityUpdateAPI(props.board.id, priorityId, values)
    notify('SUCCESS', data.detail)
    priority.value = data.priority
  } catch (error) {
    handleResponseError(error)
  } finally {
    closeEditForm()
  }
}

const openPriorityAddDropdown = ref(false)
const showPriorityAddDropdown = () => {
  openPriorityAddDropdown.value = true
}

const addNewPriority = (priority) => {
  priorities.value.push(priority)
  openPriorityAddDropdown.value = false
}

const deletePriority = async (priorityId) => {
  try {
    await priorityDeleteAPI(props.board.id, priorityId)
    notify('DELETED', 'Priority deleted successfully!', 'info')
    priorities.value = priorities.value.filter((p) => p.id !== priorityId)
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(() => {
  fetchPriorities()
})
</script>

<template>
  <WorkspaceLayout :workspace="workspace" page="boards">
    <BoardSettingsLayout
      :workspace="props.workspace"
      :board="props.board"
      page="priorities"
    >
      <div class="flex items-center justify-between">
        <div class="text-xl font-semibold">Priorities</div>
        <Dropdown :trigger="['click']" v-model:open="openPriorityAddDropdown" placement="bottomRight">
          <Button type="primary" @click="showPriorityAddDropdown">Add priority</Button>
          <template #overlay>
            <PriorityAdd :boardId="props.board.id" @created="addNewPriority" />
          </template>
        </Dropdown>
      </div>
      <Divider class="my-4" />
      <List :dataSource="priorities">
        <template #renderItem="{ item }">
          <ListItem class="group">
            <div class="w-full">
              <PriorityEdit v-if="!!selectedPriority && selectedPriority === item.id" :board="props.board" :priority="item" @close="closeEditForm" @update="updatePriority" />
              <div class="flex items-center justify-between" v-else>
                <div>
                  <FlagOutlined class="text-primary" />
                  <span class="ml-2 font-semibold">{{ item.name }}</span>
                </div>

                <div class="flex items-center gap-2 invisible group-hover:visible">
                  <Button :icon="h(EditOutlined)" size="small" type="text" @click="openPriorityEditForm(item.id)"></Button>
                  <Button
                    size="small"
                    type="text"
                  >
                  <CloseOutlined @click="deletePriority(item.id)" class="text-xs text-red-400" />
                </Button>
                </div>
              </div>
            </div>
          </ListItem>
        </template>
      </List>
    </BoardSettingsLayout>
  </WorkspaceLayout>
</template>
