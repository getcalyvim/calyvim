<script setup>
import {
  Form,
  FormItem,
  Input,
  Textarea,
  Select,
  SelectOption,
  Avatar,
  Button,
} from 'ant-design-vue'
import { h, ref } from 'vue'
import { generateAvatar, handleResponseError, notify } from '@/utils/helpers'
import { FlagOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { taskCreateAPI } from '@/utils/api'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'

const props = defineProps([
  'task',
  'boardId',
  'members',
  'priorities',
  'states',
])
const emit = defineEmits(['created'])

const getAvatarSrc = (memberId) => {
  const member = props.members.find((m) => m.id === memberId)
  return member ? member.avatar || generateAvatar(member.displayName) : ''
}

const subTaskForm = ref({
  summary: '',
  description: '',
  taskType: 'issue',
  stateId: props.states.length > 0 ? props.states[0].id : '',
  assigneeId: '',
  priorityId: null,
})
const formRef = ref()

const onSubmit = async (values) => {
  try {
    const { data } = await taskCreateAPI(props.boardId, {
      ...values,
      parentId: props.task.id,
    })
    formRef.value.resetFields()
    notify('ADDED', data.detail)
    emit('created', data.task)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <Form
    :model="subTaskForm"
    layout="vertical"
    @finish="onSubmit"
    ref="formRef"
    hideRequiredMark
  >
    <div class="grid grid-cols-4 gap-2">
      <div class="col-span-1">
        <FormItem name="stateId" label="State">
          <Select v-model:value="subTaskForm.stateId">
            <SelectOption
              :value="state.id"
              v-for="state in props.states"
              :key="state.id"
              >{{ state.name }}
            </SelectOption>
          </Select>
        </FormItem>
      </div>
      <div class="col-span-3">
        <FormItem
          name="summary"
          label="Summary"
          :rules="[{ required: true, message: 'Summary is required.' }]"
        >
          <Input v-model:value="subTaskForm.summary" />
        </FormItem>
      </div>
    </div>

    <FormItem name="description" label="Description">
      <Textarea v-model:value="subTaskForm.description" :rows="5" />
    </FormItem>

    <div class="grid grid-cols-3 gap-2">
      <FormItem name="taskType" label="Task type">
        <Select v-model:value="subTaskForm.taskType">
          <SelectOption value="issue">
            <TaskTypeIcon taskType="issue" />
            <span class="ml-2">Issue</span>
          </SelectOption>
          <SelectOption value="feature">
            <TaskTypeIcon taskType="feature" />
            <span class="ml-2">Feature</span>
          </SelectOption>
          <SelectOption value="story">
            <TaskTypeIcon taskType="story" />
            <span class="ml-2">Story</span>
          </SelectOption>
          <SelectOption value="bug">
            <TaskTypeIcon taskType="bug" />
            <span class="ml-2">Bug</span>
          </SelectOption>
        </Select>
      </FormItem>
      <FormItem name="priorityId" label="Priority">
        <Select v-model:value="subTaskForm.priorityId">
          <SelectOption :value="null">None</SelectOption>
          <SelectOption
            :value="priority.id"
            v-for="priority in props.priorities"
            :key="priority.id"
          >
            <FlagOutlined class="text-primary" />
            <span class="ml-2">
              {{ priority.name }}
            </span>
          </SelectOption>
        </Select>
      </FormItem>

      <FormItem name="assigneeId" label="Assignee">
        <Select v-model:value="subTaskForm.assigneeId" optionFilterProp="label">
          <template #tagRender="{ value }">
            <Avatar size="small" :src="getAvatarSrc(value)" />
          </template>
          <SelectOption
            v-for="member in props.members"
            :key="member.id"
            :label="member.displayName"
          >
            <div class="flex items-center gap-2">
              <Avatar
                size="small"
                :src="
                  !!member.avatar
                    ? member.avatar
                    : generateAvatar(member.displayName)
                "
              />
              <div>{{ member.displayName }}</div>
            </div>
          </SelectOption>
        </Select>
      </FormItem>
    </div>

    <div class="flex justify-end">
      <FormItem>
        <Button type="primary" :icon="h(PlusOutlined)" html-type="submit"
          >Create subtask</Button
        >
      </FormItem>
    </div>
  </Form>
</template>
