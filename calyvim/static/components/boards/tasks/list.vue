<script setup>
const props = defineProps(['workspace', 'board'])

import KanbanBoard from '@/components/boards/kanban/index.vue'
</script>

<template>
  <KanbanBoard
    :board="props.board"
    :workspace="props.workspace"
    subPage="tasks"
  />
</template>
