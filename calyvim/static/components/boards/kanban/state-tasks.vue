<script setup>
import { Card, Input, Button } from 'ant-design-vue'
import TaskCard from './task-card.vue'
import { VueDraggable } from 'vue-draggable-plus'
import { taskUpdateSequenceAPI, taskCreateAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'
import { useBoardStore } from '@/stores/board'
import { PlusOutlined } from '@ant-design/icons-vue'
import { ref } from 'vue'

const emit = defineEmits(['open', 'created'])

const props = defineProps({
  states: {
    type: Array,
    required: true,
  },
  board: {
    type: Object,
    required: true,
  },
  groupKey: {
    type: String,
    default: null,
  },
  currentSprint: {
    type: Object,
    default: null,
  },
})

const store = useBoardStore()

const updateTaskSequence = async (event, stateId) => {
  const updatedData = {
    stateId,
  }
  try {
    var state = null
    if (!!props.groupKey) {
      store.kanban.forEach((item) => {
        if (item.groupKey === props.groupKey) {
          state = item.states.find((state) => state.id === stateId)
        }
      })
    } else {
      state = store.kanban.find((state) => state.id === stateId)
    }
    if (!state) return

    const task = state.tasks[event.newIndex]

    if (event.newIndex === 0 && state.tasks.length === 1) {
      // Empty
    } else if (event.newIndex === 0) {
      updatedData['nextTask'] = state.tasks[event.newIndex + 1].id
    } else if (event.newIndex === state.tasks.length - 1) {
      updatedData['previousTask'] = state.tasks[event.newIndex - 1].id
    } else {
      updatedData['nextTask'] = state.tasks[event.newIndex + 1].id
      updatedData['previousTask'] = state.tasks[event.newIndex - 1].id
    }

    const { data } = await taskUpdateSequenceAPI(
      props.board.id,
      task.id,
      updatedData
    )
    task.sequence = data.newSequence
    task.stateId = stateId
  } catch (error) {
    handleResponseError(error)
  }
}

const newTaskTitle = ref('')
const openTaskAddForm = ref(null)
const showTaskAddForm = (stateId) => {
  openTaskAddForm.value = stateId
}
const closeTaskAddForm = () => {
  newTaskTitle.value = ''
  openTaskAddForm.value = null
}

const createTask = async (stateId, title) => {
  try {
    const newData = {
      stateId,
      summary: title,
      taskType: 'issue',
    }

    if (!!props.currentSprint) {
      newData['sprintId'] = props.currentSprint.id
    }

    if (!!props.groupKey && !!store.groupBy) {
      switch (store.groupBy) {
        case 'priority':
          newData['priorityId'] = props.groupKey
          break
        case 'assignee':
          newData['assigneeId'] = props.groupKey
          break
        case 'sprint':
          newData['sprintId'] = props.groupKey
          break
        case 'task_type':
          newData['taskType'] = props.groupKey
          break
        default:
          break
      }
    }

    const { data } = await taskCreateAPI(props.board.id, newData)
    notify('CREATED', data.detail)
    emit('created', data.task)
  } catch (error) {
    handleResponseError(error)
  } finally {
    closeTaskAddForm()
  }
}
</script>

<template>
  <div class="flex space-x-3">
    <div
      v-for="state in props.states"
      :key="state.id"
      class="rounded-lg w-[21rem] flex-shrink-0 flex flex-col"
    >
      <VueDraggable
        v-model="state.tasks"
        :group="!!props.groupKey ? props.groupKey : 'default'"
        animation="150"
        @update="(event) => updateTaskSequence(event, state.id)"
        @add="(event) => updateTaskSequence(event, state.id)"
      >
        <Card
          size="small"
          class="rounded hover:border-1 hover:border-primary transition duration-300 cursor-pointer my-2"
          v-for="task in state.tasks"
          @click="emit('open', task.id, groupKey)"
        >
          <TaskCard :board="props.board" :task="task" />
        </Card>
      </VueDraggable>
      <Card
        size="small"
        class="rounded hover:border-1 hover:border-primary transition duration-300 cursor-pointer mt-2"
        v-if="openTaskAddForm === state.id"
      >
        <Input
          v-model:value="newTaskTitle"
          :bordered="false"
          placeholder="Type your task here"
          @keyup.enter="(event) => createTask(state.id, event.target.value)"
        />
        <div class="flex justify-end">
          <Button size="small" type="text" @click="closeTaskAddForm"
            >Cancel</Button
          >
        </div>
      </Card>
      <div
        class="mb-3 cursor-pointer"
        @click="showTaskAddForm(state.id)"
        v-else
      >
        <PlusOutlined class="text-primary ml-1 mt-2" />
        <span class="text-primary"> Add Task </span>
      </div>
    </div>
  </div>
</template>
