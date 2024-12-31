<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue'
import { useBoardStore } from '@/stores/board';
import { ClockCircleOutlined } from '@ant-design/icons-vue';

const emit = defineEmits(['reload'])
const store = useBoardStore()
</script>

<template>
  <CheckboxGroup v-model:value="store.estimateFilters" class="" @change="emit('reload')">
    <div class="flex flex-col gap-1">
      <div
        class="flex items-center gap-2"
        v-for="estimate in store.estimates"
        :key="estimate.id"
      >
        <Checkbox :value="estimate.id"></Checkbox>
        <div>
          <ClockCircleOutlined class="text-xs" />
          <span class="ml-1">{{ estimate.value }}</span>
        </div>
      </div>
    </div>
  </CheckboxGroup>
</template>
