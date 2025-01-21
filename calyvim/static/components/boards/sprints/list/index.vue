<script setup>
import BoardLayout from '@/components/base/board-layout.vue'
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import {
  sprintListAPI,
  sprintActivateAPI,
  sprintDeleteAPI,
  sprintArchiveAPI,
} from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'
import { onMounted, ref, h, computed } from 'vue'
import BaseSpinner from '../../../base/base-spinner.vue'
import SprintAddForm from './sprint-add-form.vue'
import SprintAnalytics from './sprint-analytics.vue'
import { CalendarCog, CircleDashed, ChartLine } from 'lucide-vue-next'
import { useNProgress } from '@vueuse/integrations/useNProgress'

import {
  List,
  ListItem,
  Tag,
  Button,
  Dropdown,
  Menu,
  MenuItem,
  Drawer,
} from 'ant-design-vue'
import {
  ArrowRightOutlined,
  PlusOutlined,
  SyncOutlined,
  EllipsisOutlined,
  UnorderedListOutlined,
  LineChartOutlined,
  BarChartOutlined,
  InboxOutlined,
  DeleteOutlined,
} from '@ant-design/icons-vue'

const props = defineProps(['workspace', 'board'])

const sprints = ref([])
const { isLoading } = useNProgress(null, { minimum: '0.5' })
const fetchSprint = async () => {
  try {
    isLoading.value = true
    const { data } = await sprintListAPI(props.board.id)
    sprints.value = data.results
  } catch (error) {
    handleResponseError(error)
  } finally {
    isLoading.value = false
  }
}

const addSprint = (sprint) => {
  sprints.value = [sprint, ...sprints.value]
  closeSprintAddDropdown()
}

const openSprintTasks = (sprintId) => {
  window.location.href = `/boards/${props.board.id}/sprints/${sprintId}/`
}

const openSprintAddDropdown = ref(false)
const showSprintAddDropdown = () => {
  openSprintAddDropdown.value = true
}
const closeSprintAddDropdown = () => {
  openSprintAddDropdown.value = false
}

const hoveredItem = ref(null)
const setHoveredItem = (item) => {
  hoveredItem.value = item.id
}

const clearHoveredItem = () => {
  hoveredItem.value = null
}

const setActiveSprint = async (sprintId) => {
  try {
    const { data } = await sprintActivateAPI(props.board.id, sprintId)
    sprints.value = sprints.value.map((sprint) => {
      if (sprint.id === sprintId) {
        sprint.isActive = true
      } else {
        sprint.isActive = false
      }
      return sprint
    })
    notify('ACTIVATED', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}

const deleteSprint = async (sprintId) => {
  try {
    await sprintDeleteAPI(props.board.id, sprintId)
    sprints.value = sprints.value.filter((sprint) => sprint.id !== sprintId)
    notify('DELETED', 'Sprint deleted successfully')
  } catch (error) {
    handleResponseError(error)
  }
}

const archiveSprint = async (sprintId) => {
  try {
    const { data } = await sprintArchiveAPI(props.board.id, sprintId)
    sprints.value = sprints.value.filter((sprint) => sprint.id !== sprintId)
    notify('ARCHIVED', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(() => {
  fetchSprint()
})

const selectedSprintAnalytics = ref(null)
const openSprintAnalytics = ref(false)
const showSprintAnalytics = (sprintId) => {
  selectedSprintAnalytics.value = sprintId
  openSprintAnalytics.value = true
}
const closeSprintAnanlytics = () => {
  selectedSprintAnalytics.value = null
  openSprintAnalytics.value = false
}
</script>

<template>
  <BoardLayout
    :workspace="props.workspace"
    :board="props.board"
    page="boards"
    subPage="sprints"
  >
    <template #default>
      <div v-if="isLoading" class="flex justify-center items-center h-[80vh]">
        <div class="flex items-center gap-2">
          <BaseSpinner />
          <div>Please wait while we load tasks...</div>
        </div>
      </div>
      <div v-else>
        <div
          v-if="sprints.length === 0"
          class="flex justify-center items-center h-[80vh]"
        >
          <div class="flex flex-col items-center gap-4">
            <CalendarCog class="mx-auto h-16 w-16 text-primary" />
            <div class="text-gray-500">
              You haven't created any sprints yet. Get started by clicking on
              Create new sprint.
            </div>
            <Button
              type="primary"
              @click="showSprintAddDropdown"
              :icon="h(PlusOutlined)"
              >Create a new Sprint</Button
            >
          </div>
        </div>
        <div v-else>
          <List :dataSource="sprints">
            <template #renderItem="{ item }">
              <ListItem :key="item.id" class="px-2">
                <div class="flex justify-between w-full">
                  <div>
                    <SyncOutlined class="mr-2" />
                    <span>{{ item.name }}</span>
                    <Tag
                      v-if="item.isActive"
                      class="ml-2 text-primary"
                      :bordered="false"
                    >
                      Active
                    </Tag>
                  </div>

                  <div class="flex items-center gap-2">
                    <Button size="small" @click="openSprintTasks(item.id)"
                      ><span class="text-xs text-primary"
                        >View tasks</span
                      ></Button
                    >
                    <Tag :bordered="false">
                      <span>{{ item.startDate }}</span>
                      <ArrowRightOutlined />
                      <span>{{ item.endDate }}</span>
                    </Tag>
                    <Dropdown :trigger="['click']" placement="bottomRight">
                      <Button size="small" :icon="h(EllipsisOutlined)"></Button>

                      <template #overlay>
                        <Menu>
                          <MenuItem @click="openSprintTasks(item.id)">
                            <UnorderedListOutlined />
                            <span class="ml-2">View more info</span>
                          </MenuItem>
                          <MenuItem @click="showSprintAnalytics(item.id)">
                            <div class="flex items-center">
                              <ChartLine class="w-3 h-3" />
                              <div class="ml-2">View analytics</div>
                            </div>
                          </MenuItem>
                          <MenuItem @click="setActiveSprint(item.id)">
                            <div class="flex items-center">
                              <CircleDashed class="w-3 h-3" />
                              <div class="ml-2">Set as active</div>
                            </div>
                          </MenuItem>
                          <MenuItem @click="archiveSprint(item.id)">
                            <InboxOutlined />
                            <span class="ml-2">Archive sprint</span>
                          </MenuItem>
                          <MenuItem @click="deleteSprint(item.id)">
                            <DeleteOutlined class="text-red-400" />
                            <span class="ml-2 text-red-400">Delete sprint</span>
                          </MenuItem>
                        </Menu>
                      </template>
                    </Dropdown>
                  </div>
                </div>
              </ListItem>
            </template>
          </List>
        </div>
      </div>

      <!-- Analytics Drawer -->
      <Drawer
        v-model:open="openSprintAnalytics"
        placement="right"
        title="Sprint Ananlytics"
        destroyOnClose
        @close="closeSprintAnanlytics"
      >
        <SprintAnalytics
          :sprintId="selectedSprintAnalytics"
          :boardId="props.board.id"
        />
      </Drawer>
    </template>

    <template #actions>
      <div class="flex items-center me-2">
        <Dropdown
          :trigger="['click']"
          placement="bottomRight"
          v-model:open="openSprintAddDropdown"
        >
          <Button
            type="primary"
            @click="showSprintAddDropdown"
            :icon="h(PlusOutlined)"
            :disabled="sprints.length === 0"
          >
            Create Sprint
          </Button>
          <template #overlay>
            <SprintAddForm :boardId="props.board.id" @created="addSprint" />
          </template>
        </Dropdown>
      </div>
    </template>
  </BoardLayout>
</template>
