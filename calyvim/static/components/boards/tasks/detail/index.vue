<script setup>
import { onMounted, ref } from 'vue'
import { stateListAPI, boardMembersListAPI, priorityListAPI } from '@/utils/api'
import { handleResponseError } from '@/utils/helpers'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import TaskView from '@/components/boards/kanban/detail/task-view.vue'
import BoardLayout from '@/components/base/board-layout.vue'

const { isLoading } = useNProgress(null, { minimum: '0.5', initial: true })

const props = defineProps({
  board: {
    type: Object,
    required: true,
  },
  task: {
    type: Object,
    required: true,
  },
  workspace: {
    type: Object,
    required: true,
  },
})

const members = ref([])
const labels = ref([])
const priorities = ref([])
const states = ref([])

const loadMembers = async () => {
  try {
    const { data } = await boardMembersListAPI(props.board.id)
    members.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const loadLabels = async () => {}

const loadPriorities = async () => {
  try {
    const { data } = await priorityListAPI(props.board.id)
    priorities.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const loadStates = async () => {
  try {
    const { data } = await stateListAPI(props.board.id)
    states.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const loadBoardProperties = async () => {
  await loadStates()
  await loadMembers()
  await loadPriorities()
  await loadLabels()
}

onMounted(async () => {
  await loadBoardProperties()
  isLoading.value = false
})
</script>

<template>
  <div class="min-h-screen">
    <BoardLayout
      :workspace="props.workspace"
      :board="props.board"
      page="boards"
      subPage="kanban"
    >
      <template #default>
        <div v-if="!isLoading" class="flex justify-center">
          <div class="w-3/4 max-w-5xl">
            <TaskView
              :members="members"
              :states="states"
              :priorities="priorities"
              :board="props.board"
              :taskId="props.task.id"
            />
          </div>
        </div>
      </template>
    </BoardLayout>
  </div>
</template>
