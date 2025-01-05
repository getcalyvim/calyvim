<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { CircleCheckBig } from 'lucide-vue-next'
const props = defineProps(['workspace', 'currentUser'])

</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :currentUser="props.currentUser"
    page="todos"
  >
    <div class="flex justify-center items-center h-[90vh]">
      <div class="text-center mt-5">
        <CircleCheckBig class="text-primary h-12 w-12" />
        <h2 class="text-xl font-bold">Todos</h2>
        <h2 class="text-lg font-semibold">
          This feature is currently being developed, we will be right back soon.
        </h2>
        <p class="text">
          This feature helps you manage your tasks and to-dos efficiently. Stay organized and keep track of your work with ease.
        </p>
      </div>
    </div>
  </WorkspaceLayout>
</template>
