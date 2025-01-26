<script setup>
import { BorderOutlined, EllipsisOutlined } from '@ant-design/icons-vue'
import { Button, Dropdown } from 'ant-design-vue'
import { h } from 'vue'
import StateMenu from '@/components/boards/kanban/state-menu.vue'

const props = defineProps(['states', 'board'])
</script>

<template>
  <div class="flex space-x-3">
    <div
      v-for="state in states"
      :key="state.id"
      class="rounded-lg w-[21rem] flex-shrink-0"
    >
      <div
        class="font-bold mb-2 bg-gray-200 rounded px-2 py-1 flex justify-between items-center"
      >
        <div>
          <BorderOutlined class="text-primary" />
          <span class="ml-2">{{ state.name }}</span>
        </div>

        <div>
          <Dropdown :trigger="['click']">
            <Button :icon="h(EllipsisOutlined)" size="small" type="text" />
            <template #overlay>
              <StateMenu :state="state" :board="props.board" />
            </template>
          </Dropdown>
        </div>
      </div>
    </div>
  </div>
</template>
