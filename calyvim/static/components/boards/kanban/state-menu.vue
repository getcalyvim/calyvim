<script setup>
import { DoubleRightOutlined, FolderOpenOutlined } from '@ant-design/icons-vue'
import { Menu, MenuItem, SubMenu } from 'ant-design-vue'
import { ref } from 'vue';

import { useKanbanStore } from '@/stores/kanban'

const props = defineProps(['state'])

const store = useKanbanStore()
</script>

<template>
  <Menu>
    <SubMenu>
      <template #title>
        <DoubleRightOutlined />
        <span class="ml-2">Move all tasks to another state</span>
      </template>

      <MenuItem v-for="state in store.states" :key="state.id" :disabled="state.id === props.state.id">
        {{ state.name }}
      </MenuItem>
    </SubMenu>
    <MenuItem>
      <FolderOpenOutlined />
      <span class="ml-2">Archive all tasks in the {{ props.state.name }}</span>
    </MenuItem>
  </Menu>
</template>
