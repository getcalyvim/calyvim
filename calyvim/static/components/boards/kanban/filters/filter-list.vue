<script setup>
import { Card, Divider } from 'ant-design-vue'

import { useBoardStore } from '@/stores/board'
import TaskTypeFilters from './task-type-filters.vue'
import AssigneeFilters from './assignee-filters.vue'
import PriorityFilters from './priority-filters.vue'
import LabelFilters from './label-filters.vue'
import EstimateFilters from './estimate-filters.vue'
import SprintFilters from './sprint-filters.vue'
import { computed } from 'vue'

const store = useBoardStore()

const emit = defineEmits(['reload'])
const props = defineProps({
  board: {
    type: Object,
    required: true,
  },
  currentSprint: {
    type: Object,
    required: false,
    default: null,
  },
})

const hasCurrentSprint = computed(() => props.currentSprint !== null)
</script>

<template>
  <Card class="w-80 max-h-[45rem] overflow-y-auto" title="Filters" size="small">
    <div v-if="!store.groupBy || store.groupBy !== 'priority'">
      <div class="font-semibold text-gray-600">Priorities</div>
      <PriorityFilters @reload="emit('reload')" />
      <Divider class="my-2 p-0" />
    </div>

    <template v-if="!store.groupBy || store.groupBy !== 'assignee'">
      <div>
        <div class="font-semibold text-gray-600">Assignees</div>
        <AssigneeFilters @reload="emit('reload')" />
      </div>
      <Divider class="my-2 p-0" />
    </template>

    <template v-if="props.board.isEstimateEnabled">
      <div>
        <div class="font-semibold text-gray-600">Estimates</div>
        <EstimateFilters @reload="emit('reload')" />
      </div>
      <Divider class="my-2 p-0" />
    </template>

    <template v-if="!hasCurrentSprint">
      <div>
        <div class="font-semibold text-gray-600">Sprints</div>
        <SprintFilters @reload="emit('reload')" />
      </div>
      <Divider class="my-2 p-0" />
    </template>

    <div>
      <div class="font-semibold text-gray-600">Types</div>
      <TaskTypeFilters @reload="emit('reload')" />
      <Divider class="my-2 p-0" />
    </div>

    <div>
      <div class="font-semibold text-gray-600">Labels</div>
      <LabelFilters @reload="emit('reload')" />
    </div>
  </Card>
</template>
