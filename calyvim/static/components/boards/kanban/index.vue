<script setup>
import BoardLayout from '@/components/base/board-layout.vue'
import { useBoardStore } from '@/stores/board'
import { h, onMounted, ref } from 'vue'
import {
  boardUpdateAPI,
  taskListKanbanAPI,
  boardMetadataAPI,
} from '@/utils/api'
import { handleResponseError, generateAvatar } from '@/utils/helpers'
import {
  Button,
  Dropdown,
  Avatar,
  Drawer,
  Tag,
  Select,
  AvatarGroup,
} from 'ant-design-vue'
import {
  FilterOutlined,
  PlusOutlined,
  SyncOutlined,
  FlagOutlined,
  UserOutlined,
  ArrowDownOutlined,
  ArrowRightOutlined,
  CarryOutOutlined,
  BlockOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons-vue'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import FilterList from '@/components/boards/kanban/filters/filter-list.vue'
import TaskAddForm from '@/components/boards/kanban/task-add-form.vue'
import TaskView from '@/components/boards/kanban/detail/task-view.vue'
import StateMenu from './state-menu.vue'
import StateTaskSkeletonLoader from './state-task-skeleton-loader.vue'
import StateList from './state-list.vue'
import StateTasks from './state-tasks.vue'

const props = defineProps({
  workspace: {
    type: Object,
    required: true,
  },
  board: {
    type: Object,
    required: true,
  },
  currentSprint: {
    type: Object,
    required: false,
    default: null,
  },
  currentTab: {
    type: String,
    default: 'kanban',
  },
  subPage: {
    type: String,
    default: 'kanban',
  }
})

const openFilterDropdown = ref(false)
const openTaskAddDropdown = ref(false)

const openedGroups = ref(new Set())
const defaultFilters = {
  sprints: props.currentSprint ? [props.currentSprint.id] : [],
}

const toggleGroup = (groupKey) => {
  if (openedGroups.value.has(groupKey)) {
    openedGroups.value.delete(groupKey)
  } else {
    openedGroups.value.add(groupKey)
  }
}

const { isLoading } = useNProgress(null, { minimum: '0.5' })
const taskLoading = ref(false)

const store = useBoardStore()

const loadTasks = async (filters = {}) => {
  try {
    taskLoading.value = true
    const { data } = await taskListKanbanAPI(props.board.id, {
      groupBy: store.groupBy,
      ...filters,
      ...defaultFilters,
    })

    store.initializeKanban(data.results)
    data.results.forEach((item) => {
      openedGroups.value.add(item.groupKey)
    })
  } catch (error) {
    handleResponseError(error)
  } finally {
    taskLoading.value = false
  }
}

const loadMetadata = async () => {
  try {
    const { data } = await boardMetadataAPI(props.board.id)
    const metadata = data.metadata

    store.initializeStates(metadata.states)
    store.initializeMembers(metadata.members)
    store.initializePriorities(metadata.priorities)
    store.initializeLabels(metadata.labels)
    store.initializeSprints(metadata.sprints)
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(async () => {
  isLoading.value = true

  await loadMetadata()
  await store.initializeGroupBy(props.board.currentGroupBy)
  await loadTasks()

  isLoading.value = false
})

const taskViewId = ref(null)
const taskViewGroupKey = ref(null)
const showTaskView = ref(false)
const openTaskView = (taskId, groupKey) => {
  taskViewId.value = taskId
  taskViewGroupKey.value = groupKey
  showTaskView.value = true
}
const closeTaskView = () => {
  showTaskView.value = false
  taskViewId.value = null
  taskViewGroupKey.value = null
}

const loadTaskAndUpdateCurrentGroupBy = async (value) => {
  isLoading.value = true

  await store.clearFilters()
  await loadTasks()

  isLoading.value = false

  boardUpdateAPI(props.board.id, {
    currentGroupBy: value,
  })
}

const updateTask = async (taskId, updatedData) => {
  for (const [key, value] of Object.entries(updatedData)) {
    switch (key) {
      case 'priorityId':
        const priority = store.priorities.find((p) => p.id === value)
        updatedData['priority'] = priority

        store.updateTask(
          taskId,
          updatedData,
          'priority',
          value === null ? 'no_priority' : value
        )
        break

      case 'stateId':
        const state = store.states.find((s) => s.id === value)
        updatedData['state'] = state

        store.updateTask(taskId, updatedData)
        if (!!taskViewGroupKey.value) {
          store.updateTaskPositionByGroup(
            taskId,
            value,
            taskViewGroupKey.value,
            updatedData
          )
        } else {
          store.updateTaskPosition(taskId, value, updatedData)
        }
        break

      case 'assigneeId':
        const assignee = store.members.find((m) => m.id === value)

        updatedData['assignee'] = assignee
        store.updateTask(
          taskId,
          updatedData,
          'assignee',
          value === null ? 'no_assignee' : value
        )
        break

      case 'sprintId':
        const sprint = store.sprints.find((s) => s.id === value)
        updatedData['sprint'] = sprint

        store.updateTask(
          taskId,
          updatedData,
          'sprint',
          value === null ? 'no_sprint' : value
        )
        break

      case 'taskType':
        store.updateTask(taskId, updatedData, 'task_type', value)
        break

      default:
        store.updateTask(taskId, updatedData)
        break
    }
  }
}

const reloadTasks = async () => {
  isLoading.value = true
  await loadTasks({
    assignees: store.assigneeFilters,
    taskTypes: store.taskTypes,
    priorities: store.priorityFilters,
    labels: store.labelFilters,
    estimates: store.estimateFilters,
    sprints: store.sprintFilters,
  })
  isLoading.value = false
}

const addNewTask = (task) => {
  openTaskAddDropdown.value = false
  store.addTask(task)
}
</script>

<template>
  <div class="min-h-screen">
    <BoardLayout
      :workspace="props.workspace"
      :board="props.board"
      page="boards"
      :subPage="props.subPage"
    >
      <template #actions>
        <div class="flex items-center gap-3 mx-2">
          <div class="flex items-center gap-1">
            <AvatarGroup class="mr-3" :maxCount="7" size="small">
              <Avatar
                size="small"
                v-for="member in store.members"
                :key="member.id"
                :src="
                  !!member.avatar
                    ? member.avatar
                    : generateAvatar(member.displayName)
                "
                :title="member.displayName"
              />
            </AvatarGroup>
            <div class="font-semibold text-xs text-gray-500">Group by</div>
            <Select
              v-model:value="store.groupBy"
              class="w-36"
              @change="loadTaskAndUpdateCurrentGroupBy"
            >
              <Select.Option :value="null">None</Select.Option>
              <Select.Option value="assignee">
                <UserOutlined class="text-primary" />
                <span class="ml-2">Assignee</span>
              </Select.Option>
              <Select.Option value="priority">
                <FlagOutlined class="text-primary" />
                <span class="ml-2">Priority</span>
              </Select.Option>
              <Select.Option value="sprint" :disabled="!!props.currentSprint">
                <CarryOutOutlined class="text-primary" />
                <span class="ml-2">Sprint</span>
              </Select.Option>
              <Select.Option value="task_type">
                <BlockOutlined class="text-primary" />
                <span class="ml-2">Task type</span>
              </Select.Option>
              <Select.Option value="estimate">
                <ClockCircleOutlined class="text-primary" />
                <span class="ml-2">Estimate</span>
              </Select.Option>
            </Select>
          </div>
          <Dropdown
            :trigger="['click']"
            placement="bottomRight"
            v-model:open="openFilterDropdown"
          >
            <Button :icon="h(FilterOutlined)">Filters</Button>
            <template #overlay>
              <FilterList
                :board="props.board"
                @reload="reloadTasks"
                :currentSprint="props.currentSprint"
              />
            </template>
          </Dropdown>
          <Dropdown
            :trigger="['click']"
            placement="bottomRight"
            v-model:open="openTaskAddDropdown"
          >
            <Button type="primary" :icon="h(PlusOutlined)">Add task</Button>
            <template #overlay>
              <TaskAddForm
                :board="props.board"
                @created="addNewTask"
                :currentSprint="props.currentSprint"
              />
            </template>
          </Dropdown>
        </div>
      </template>
      <template #default>
        <div class="w-full overflow-x-auto">
          <div class="min-w-max px-1">
            <StateList :states="store.states" />
            <template v-if="taskLoading">
              <div class="task-list">
                <StateTaskSkeletonLoader :states="store.states" />
              </div>
            </template>
            <template v-else>
              <!-- For Group By - Assignee -->
              <div
                v-if="!!store.groupBy && store.groupBy === 'assignee'"
                class="task-list"
              >
                <div
                  class="w-full mb-1"
                  v-for="item in store.kanban"
                  :key="item.id"
                >
                  <template v-if="item.groupBy === 'assignee'">
                    <div class="bg-gray-100 px-2 py-1 rounded">
                      <Button
                        type="text"
                        size="small"
                        class="mr-2"
                        @click="toggleGroup(item.groupKey)"
                      >
                        <ArrowRightOutlined
                          v-if="!openedGroups.has(item.groupKey)"
                          class="text-xs text-gray-500"
                        />
                        <ArrowDownOutlined
                          v-else
                          class="text-xs text-gray-500"
                        />
                      </Button>
                      <template v-if="!!item.assignee">
                        <Avatar
                          :src="
                            !!item.assignee.avatar
                              ? item.assignee.avatar
                              : generateAvatar(item.assignee.displayName)
                          "
                          :size="24"
                        />
                        <span class="ml-2">{{
                          item.assignee.displayName
                        }}</span>
                      </template>
                      <template v-else>
                        <UserOutlined class="text-primary" />
                        <span class="ml-2">Unassigned</span>
                      </template>
                    </div>

                    <StateTasks
                      v-if="openedGroups.has(item.groupKey)"
                      :states="item.states"
                      :board="props.board"
                      :groupKey="item.groupKey"
                      @open="openTaskView"
                      @created="(newTask) => store.addTask(newTask)"
                      :currentSprint="props.currentSprint"
                    />
                  </template>
                </div>
              </div>

              <!-- For Group By - Priority -->
              <div
                v-else-if="!!store.groupBy && store.groupBy === 'priority'"
                class="task-list"
              >
                <div
                  class="w-full mb-1"
                  v-for="item in store.kanban"
                  :key="item.id"
                >
                  <template v-if="item.groupBy === 'priority'">
                    <div class="bg-gray-100 px-2 py-1 rounded">
                      <Button
                        type="text"
                        size="small"
                        class="mr-2"
                        @click="toggleGroup(item.groupKey)"
                      >
                        <ArrowRightOutlined
                          v-if="!openedGroups.has(item.groupKey)"
                          class="text-xs text-gray-500"
                        />
                        <ArrowDownOutlined
                          v-else
                          class="text-xs text-gray-500"
                        />
                      </Button>
                      <FlagOutlined class="text-primary" />
                      <span class="ml-2 font-semibold" v-if="!!item.priority">
                        {{ item.priority.name }}
                      </span>
                      <span v-else class="font-semibold"> Unprioritized </span>
                    </div>

                    <StateTasks
                      v-if="openedGroups.has(item.groupKey)"
                      :states="item.states"
                      :board="props.board"
                      :groupKey="item.groupKey"
                      @open="openTaskView"
                      @created="(newTask) => store.addTask(newTask)"
                      :currentSprint="props.currentSprint"
                    />
                  </template>
                </div>
              </div>

              <!-- For Group By - Task Type -->
              <div
                v-else-if="!!store.groupBy && store.groupBy === 'task_type'"
                class="task-list"
              >
                <div
                  class="w-full mb-1"
                  v-for="item in store.kanban"
                  :key="item.id"
                >
                  <template v-if="item.groupBy === 'task_type'">
                    <div class="bg-gray-100 px-2 py-1 rounded">
                      <Button
                        type="text"
                        size="small"
                        class="mr-2"
                        @click="toggleGroup(item.groupKey)"
                      >
                        <ArrowRightOutlined
                          v-if="!openedGroups.has(item.groupKey)"
                          class="text-xs text-gray-500"
                        />
                        <ArrowDownOutlined
                          v-else
                          class="text-xs text-gray-500"
                        />
                      </Button>
                      <BlockOutlined class="text-primary" />
                      <span class="ml-2 font-semibold">
                        {{ item.taskType }}
                      </span>
                    </div>

                    <StateTasks
                      v-if="openedGroups.has(item.groupKey)"
                      :states="item.states"
                      :board="props.board"
                      :groupKey="item.groupKey"
                      @open="openTaskView"
                      @created="(newTask) => store.addTask(newTask)"
                      :currentSprint="props.currentSprint"
                    />
                  </template>
                </div>
              </div>

              <!-- Group By - Sprint -->
              <div
                v-else-if="!!store.groupBy && store.groupBy === 'sprint'"
                class="task-list"
              >
                <div
                  class="w-full mb-1"
                  v-for="item in store.kanban"
                  :key="item.id"
                >
                  <template v-if="item.groupBy === 'sprint'">
                    <div
                      class="bg-gray-100 px-2 py-1 rounded flex items-center"
                    >
                      <Button
                        type="text"
                        size="small"
                        class="mr-2"
                        @click="toggleGroup(item.groupKey)"
                      >
                        <ArrowRightOutlined
                          v-if="!openedGroups.has(item.groupKey)"
                          class="text-xs text-gray-500"
                        />
                        <ArrowDownOutlined
                          v-else
                          class="text-xs text-gray-500"
                        />
                      </Button>
                      <SyncOutlined class="text-primary" />
                      <div class="ml-2 font-semibold" v-if="!!item.sprint">
                        {{ item.sprint.name }}
                      </div>
                      <div v-else class="font-semibold ml-2">No Sprint</div>
                      <Tag
                        v-if="!!item.sprint && item.sprint.isActive"
                        :bordered="false"
                        class="ml-1 text-primary"
                        >Active</Tag
                      >
                    </div>

                    <StateTasks
                      v-if="openedGroups.has(item.groupKey)"
                      :states="item.states"
                      :board="props.board"
                      :groupKey="item.groupKey"
                      @open="openTaskView"
                      @created="(newTask) => store.addTask(newTask)"
                      :currentSprint="props.currentSprint"
                    />
                  </template>
                </div>
              </div>

              <!-- For Group By - None (Normal Board) -->
              <div v-else class="task-list">
                <StateTasks
                  :states="store.kanban"
                  :board="props.board"
                  @open="openTaskView"
                  @created="(newTask) => store.addTask(newTask)"
                  :currentSprint="props.currentSprint"
                />
              </div>
            </template>
          </div>
        </div>

        <!-- TaskViewDrawer -->
        <Drawer
          centered
          v-model:open="showTaskView"
          destroyOnClose
          @close="closeTaskView"
          :header-style="{ display: 'none' }"
          :width="920"
        >
          <TaskView
            :board="props.board"
            :taskId="taskViewId"
            :members="store.members"
            :priorities="store.priorities"
            :states="store.states"
            :sprints="store.sprints"
            :labels="store.labels"
            @update="updateTask"
          />
        </Drawer>
      </template>
    </BoardLayout>
  </div>
</template>

<style scoped>
.board-container {
  overflow-x: auto;
}

.task-list {
  /* min-height: 50px; */
  height: calc(100vh - 118px);
  overflow-y: auto;
}

/* Custom scrollbar styles */
.task-list::-webkit-scrollbar {
  width: 8px;
}

.task-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.task-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.task-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* For Firefox */
.task-list {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}
</style>
