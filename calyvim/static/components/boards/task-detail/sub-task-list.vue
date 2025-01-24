<script setup>
// import { useKanbanStore } from '@/stores/kanban'
import { Avatar, Divider, Select, SelectOption, Tag } from 'ant-design-vue'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { handleResponseError, generateAvatar } from '@/utils/helpers'
import { taskUpdateAPI } from '@/utils/api'
import { computed, ref } from 'vue'

const props = defineProps(['subtasks', 'boardId', 'states', 'members'])
const emit = defineEmits(['selected'])

const handleStateChange = async (value, taskId) => {
  try {
    await taskUpdateAPI(props.boardId, taskId, { stateId: value })
  } catch (error) {
    handleResponseError(error)
  }
}

const openSubTask = (taskId) => {
  emit('selected', taskId)
}

const memberOptions = computed(() =>
  props.members.map((member) => ({
    value: member.id,
    label: member.avatar || generateAvatar(member.displayName),
    name: member.displayName,
  }))
)

const getAvatarSrc = (memberId) => {
  const member = props.members.find((m) => m.id === memberId)
  return member ? member.avatar || generateAvatar(member.displayName) : ''
}
</script>

<template>
  <div v-if="props.subtasks.length > 0">
    <Divider />
    <div class="text-lg font-semibold">Subtasks</div>
    <div v-for="task in props.subtasks" :key="task.id">
      <div class="flex justify-between items-center px-3 py-2 rounded shadow">
        <div class="flex gap-2 items-center">
          <TaskTypeIcon :taskType="task.taskType" />
          <div
            class="font-semibold hover:underline hover:underline-offset-1 text-primary cursor-pointer"
            @click="openSubTask(task.id)"
          >
            {{ task.name }}
          </div>
          <div
            class="font-semibold hover:underline hover:underline-offset-1 cursor-pointer"
            @click="openSubTask(task.id)"
          >
            {{ task.summary }}
          </div>
        </div>
        <div class="flex gap-3 items-center">
          <div class="text-xs font-semibold">{{ task?.priority?.name }}</div>
          <Avatar
            :size="22"
            :src="
              !!task.assignee.avatar
                ? task.assignee.avatar
                : generateAvatar(task.assignee.displayName)
            "
            v-if="!!task.assignee"
          />
          <Avatar :size="22" v-else />
          <Select
            v-model:value="task.stateId"
            size="small"
            style="width: 100px"
            @change="(value) => handleStateChange(value, task.id)"
          >
            <SelectOption
              :value="state.id"
              v-for="state in props.states"
              :key="state.id"
              >{{ state.name }}
            </SelectOption>
          </Select>
        </div>
      </div>
    </div>
  </div>
</template>
