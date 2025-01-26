<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue'
import { useBoardStore } from '@/stores/board'
import { SyncOutlined } from '@ant-design/icons-vue'

const emit = defineEmits(['reload'])
const store = useBoardStore()
</script>

<template>
  <CheckboxGroup v-model:value="store.sprintFilters" class="" @change="emit('reload')">
    <div class="flex flex-col gap-1">
      <div
        class="flex items-center gap-2"
        v-for="sprint in store.sprints"
        :key="sprint.id"
      >
        <Checkbox :value="sprint.id"></Checkbox>
        <div>
          <SyncOutlined class="text-xs" />
          <span class="ml-1">{{ sprint.name }}</span>
        </div>
      </div>
    </div>
  </CheckboxGroup>
</template>
