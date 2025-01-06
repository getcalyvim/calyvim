<script setup>
import { CheckCircle, PlayCircle, BugPlay, PlusCircle } from 'lucide-vue-next'

BugPlay
const props = defineProps(['taskType']);
</script>

<template>
  <CheckCircle class="text-primary w-3 h-3" v-if="props.taskType === 'issue'" />
  <PlayCircle class="text-primary w-3 h-3" v-else-if="props.taskType === 'story'" />
  <BugPlay class="text-primary w-3 h-3" v-else-if="props.taskType === 'bug'" />
  <PlusCircle class="text-primary w-3 h-3" v-else-if="props.taskType === 'feature'" />
</template>