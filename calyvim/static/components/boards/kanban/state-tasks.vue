<script setup>
import { Card } from 'ant-design-vue'
import TaskCard from './task-card.vue'
import { VueDraggable } from 'vue-draggable-plus'
import { taskUpdateSequenceAPI } from '@/utils/api'
import { handleResponseError } from '@/utils/helpers'
import { useBoardStore } from '@/stores/board'

const emit = defineEmits(['open'])

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
})

const store = useBoardStore()

const updateTaskSequence = async (event, stateId) => {
  console.log('Event --', event)
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
</script>

<template>
  <div class="flex space-x-3">
    <VueDraggable
      v-for="state in states"
      :key="state.id"
      v-model="state.tasks"
      :group="!!props.groupKey ? props.groupKey : 'default'"
      class="rounded-lg w-[21rem] flex-shrink-0 py-2 flex flex-col gap-2"
      @update="(event) => updateTaskSequence(event, state.id)"
      @add="(event) => updateTaskSequence(event, state.id)"
    >
      <Card
        size="small"
        class="rounded hover:border-1 hover:border-primary transition duration-300 cursor-pointer"
        v-for="task in state.tasks"
        @click="emit('open', task.id, groupKey)"
      >
        <TaskCard :board="props.board" :task="task" />
      </Card>
    </VueDraggable>
  </div>
</template>
