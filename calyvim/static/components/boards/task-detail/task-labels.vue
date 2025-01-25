<script setup>
import { Tag, Button, Dropdown, Menu, MenuItem, Badge } from 'ant-design-vue'
import { X, Plus } from 'lucide-vue-next'
import { computed } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
  labels: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['deleteLabel'])
const availableTags = computed(() =>
  props.labels.filter((label) => {
    return !props.task.labels.some((taskLabel) => taskLabel.id === label.id)
  })
)
</script>

<template>
  <div class="flex gap-1 items-center mb-1">
    <Tag
      v-for="label in props.task.labels"
      :key="label.id"
      :bordered="false"
      class="flex items-center gap-1"
    >
      <div
        class="h-1 w-1 rounded-full"
        :style="{ backgroundColor: label.color }"
      ></div>
      <div class="text-xs my-1 leading-none font-semibold">
        {{ label.name }}
      </div>
      <X
        class="h-3 w-3 cursor-pointer"
        @click="emit('deleteLabel', label.id)"
      />
    </Tag>
    <Dropdown :trigger="['click']">
      <Button type="text" size="small">
        <template #icon>
          <Plus class="h-4 w-4 align-middle" />
        </template>
      </Button>

      <template #overlay>
        <Menu>
          <MenuItem
            v-for="tag in availableTags"
            :key="tag.id"
            @click="emit('addLabel', tag.id)"
          >
            <Badge :color="tag.color" />
            <span>{{ tag.name }}</span>
          </MenuItem>
        </Menu>
      </template>
    </Dropdown>
  </div>
</template>
