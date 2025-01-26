<script setup>
const props = defineProps(['workspace', 'board', 'sprint'])

import KanbanBoard from '@/components/boards/tasks/list/index.vue'
</script>

<template>
  <KanbanBoard
    :board="props.board"
    :workspace="props.workspace"
    :currentSprint="props.sprint"
    subPage="sprints"
  />
</template>
