<script setup>
import { Card } from 'ant-design-vue'
import TaskCard from './task-card.vue'
import { VueDraggable } from 'vue-draggable-plus'

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
        default: null
    }
})
</script>

<template>
  <div class="flex space-x-3">
    <VueDraggable
      v-for="state in states"
      :key="state.id"
      v-model="state.tasks"
      :group="!!props.groupKey ? props.groupKey : 'default'"
      class="rounded-lg w-[21rem] flex-shrink-0 py-2 flex flex-col gap-2"
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
