<script setup>
import { h, onMounted, ref, watch } from 'vue'
import {
  Skeleton,
  Avatar,
  Button,
  Radio,
  RadioGroup,
  Divider,
  Dropdown,
  Menu,
  MenuItem,
  Upload,
  message,
  Modal,
  Alert,
} from 'ant-design-vue'
import {
  EllipsisOutlined,
  SaveOutlined,
  ShareAltOutlined,
  SyncOutlined,
  LeftSquareOutlined,
  PlusOutlined,
  SwitcherOutlined,
  LinkOutlined,
  CheckSquareOutlined,
  FileOutlined,
  ArrowLeftOutlined,
} from '@ant-design/icons-vue'
import {
  handleResponseError,
  generateAvatar,
  notify,
  uploadRequestHandler,
} from '@/utils/helpers'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import debounce from 'lodash/debounce'

// Component imports
import TaskCommentList from './task-comment-list.vue'
import SubTaskAddForm from './sub-task-add-form.vue'
import TextEditor from '@/components/base/text-editor.vue'
import TaskActionBar from './task-action-bar.vue'
import TaskCommentAddForm from './task-comment-add-form.vue'
import TaskAttachmentList from './task-attachment-list.vue'
import SubTaskList from './sub-task-list.vue'

// API imports
import {
  taskCommentsAPI,
  taskAttachmentsDeleteAPI,
  taskDetailAPI,
  taskUpdateAPI,
  taskAttachmentsCreateAPI,
  taskAttachmentsListAPI,
  taskListAPI,
  taskArchiveApi,
} from '@/utils/api'
import TaskTypeIcon from '../../../icons/task-type-icon.vue'

// Setup dayjs
dayjs.extend(relativeTime)

// Props
const props = defineProps({
  board: {
    type: Object,
    required: true,
  },
  taskId: {
    type: String,
    required: true,
  },
  members: {
    type: Array,
    default: () => [],
  },
  priorities: {
    type: Array,
    default: () => [],
  },
  states: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update', 'selected'])

// State
const loading = ref(false)
const updateLoading = ref(false)
const selectedCommentType = ref('update')
const task = ref(null)
const comments = ref([])
const attachments = ref([])
const subtasks = ref([])
const showSubtaskAddForm = ref(false)
const openDescriptionActionButton = ref(false)
const isArchived = ref(false)

// Task Management
const loadTask = async (taskId) => {
  try {
    const { data } = await taskDetailAPI(props.board.id, taskId)
    task.value = {
      ...data,
      oldStateId: data.stateId,
    }
  } catch (error) {
    handleResponseError(error)
  }
}

// Comments Management
const loadComments = async (taskId) => {
  try {
    const { data } = await taskCommentsAPI(
      props.board.id,
      taskId,
      selectedCommentType.value
    )
    comments.value = data.map((comment) => ({
      ...comment,
      key: comment.id,
    }))
  } catch (error) {
    handleResponseError(error)
  }
}

const logComment = (commentLog) => {
  if (
    selectedCommentType.value === 'activity' ||
    selectedCommentType.value === 'all'
  ) {
    comments.value.unshift(commentLog)
  }
}

const addNewComment = (newComment) => {
  if (
    selectedCommentType.value === 'all' ||
    selectedCommentType.value === 'update'
  ) {
    comments.value.unshift(newComment)
  }
}

const handleCommentTypeChange = () => {
  loadComments()
}

// Attachments Management
const loadAttachments = async (taskId) => {
  try {
    const { data } = await taskAttachmentsListAPI(props.board.id, taskId)
    attachments.value = data
  } catch (error) {
    handleResponseError(error)
  }
}

const createAttachment = async (options) => {
  const { fileKey, fileSrc } = await uploadRequestHandler(
    options,
    'TaskAttachment',
    'attachment'
  )

  try {
    const { data } = await taskAttachmentsCreateAPI(
      props.board.id,
      props.taskId,
      {
        attachment: fileKey,
        filename: options.file.name,
        mimeType: options.file.type,
      }
    )
    attachments.value.push({
      ...data.attachment,
      attachment: fileSrc,
    })
    notify('ADDED', data.detail)
    // message.success(`You have added an attachment to ${task.value.name}`)
    logComment(data.comment)
  } catch (error) {
    handleResponseError(error)
  }
}

const deleteAttachment = async (attachmentId) => {
  try {
    const { data } = await taskAttachmentsDeleteAPI(
      props.board.id,
      props.taskId,
      attachmentId
    )
    attachments.value = attachments.value.filter(
      (attachment) => attachment.id !== attachmentId
    )
    notify('REMOVED', data.detail)
    logComment(data.comment)
  } catch (error) {
    handleResponseError(error)
  }
}

// Description Management
const showDescriptionActionButton = () => {
  openDescriptionActionButton.value = true
}

const closeDescriptionActionButton = () => {
  openDescriptionActionButton.value = false
}

const updateDescription = () => {
  updateTaskItem({ description: task.value.description })
  closeDescriptionActionButton()
}

// Summary Management
const updateSummary = (event) => {
  updateTaskItem({ summary: event.target.innerText })
}

const debouncedUpdateSummary = debounce(updateSummary, 1000)

// Subtask Management
const openSubtaskAddForm = () => {
  showSubtaskAddForm.value = true
}

const closeSubtaskAddForm = () => {
  showSubtaskAddForm.value = false
}

const loadSubTasks = async (taskId) => {
  try {
    const { data } = await taskListAPI(props.board.id, {
      parentId: taskId,
    })
    subtasks.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const addTaskToSubtask = (data) => {
  closeSubtaskAddForm()
  subtasks.value.push(data)
}

// Loading and Initialization
const loadTaskDetails = async (taskId) => {
  loading.value = true
  await loadTask(taskId)
  await loadComments(taskId)
  await loadAttachments(taskId)
  await loadSubTasks(taskId)
  loading.value = false
}

// Lifecycle Hooks
onMounted(() => {
  loadTaskDetails(props.taskId)
})

const updateTaskv2 = async (updatedData) => {
  try {
    const { data } = await taskUpdateAPI(
      props.board.id,
      props.taskId,
      updatedData
    )
    notify('UPDATED', data.log)
    logComment(data.log)
  } catch (error) {
    handleResponseError(error)
  }
}

const updateTaskItem = async (updatedData) => {
  await updateTaskv2(updatedData)
  await emit('update', props.taskId, updatedData)
}

const openTask = async (taskId) => {
  emit('selected', taskId)
  await loadTaskDetails(taskId)
}
</script>

<template>
  <div v-if="!!task && !loading">
    <div class="mb-4">
      <!-- Archive Banner -->
      <div
        v-if="isArchived"
        class="bg-gray-300 border-l-4 border-gray-500 text-gray-700 px-2 py-3 flex items-center rounded"
        role="alert"
      >
        <div class="font-semibold">
          <span class="font-bold">Warning: </span> This task has been archived.
        </div>
      </div>

      <div v-if="!!task.parentId" class="cursor-pointer mb-2" @click="openTask(task.parentId)">
        <ArrowLeftOutlined />
        <span class="ml-2">Back to parent task</span>
      </div>

      <div class="flex items-center justify-between">
        <div class="text-base font-bold">
          <TaskTypeIcon :taskType="task.taskType" />
          {{ task.name }}
        </div>
        <div class="flex gap-2 items-center">
          <div v-if="updateLoading" class="text-gray-400">
            <SyncOutlined />
            <span class="ml-2">Saving</span>
          </div>
          <Button :icon="h(ShareAltOutlined)" type="text">Share</Button>
          <Button :icon="h(EllipsisOutlined)" type="text"></Button>
        </div>
      </div>

      <div
        class="text-2xl font-semibold mb-1"
        contenteditable="true"
        @input="debouncedUpdateSummary"
      >
        {{ task.summary }}
      </div>

      <div class="text-sm text-gray-500">
        <div class="flex items-center gap-1 text-xs">
          <div>Created on</div>
            <div>{{ dayjs(task.createdAt).format('MMMM D, YYYY') }} by</div>
          <Avatar
            :size="16"
            :src="
              !!task.createdBy.avatar
                ? task.createdBy.avatar
                : generateAvatar(task.createdBy.displayName)
            "
          />
          <div>{{ task.createdBy.displayName }}</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-9">
        <div class="mb-5">
          <Dropdown :trigger="['click']" placement="rightTop">
            <Button :icon="h(PlusOutlined)" type="primary"
              ><span class="font-semibold">Add</span></Button
            >
            <template #overlay>
              <Menu>
                <MenuItem key="subtask" @click="openSubtaskAddForm">
                  <SwitcherOutlined />
                  Subtask
                </MenuItem>

                <MenuItem key="attachment">
                  <Upload
                    :multiple="false"
                    name="file"
                    :customRequest="createAttachment"
                  >
                    <template #itemRender="{ file, actions }">
                      <!-- Don't render anything -->
                    </template>
                    <FileOutlined />
                    Attachment
                  </Upload>
                </MenuItem>

                <MenuItem key="checklist" disabled>
                  <CheckSquareOutlined />
                  Checklist (Coming Soon)
                </MenuItem>

                <MenuItem key="link" disabled>
                  <LinkOutlined />
                  Link (Coming Soon)
                </MenuItem>
              </Menu>
            </template>
          </Dropdown>
        </div>

        <div class="text-lg font-semibold">Description</div>
        <div>
          <TextEditor v-model="task.description" @saved="updateDescription" />
        </div>

        <div class="mb-4">
          <TaskAttachmentList
            :boardId="props.board.id"
            :taskId="props.taskId"
            :attachments="attachments"
            @delete="deleteAttachment"
          />
        </div>

        <div class="mb-4">
          <SubTaskList
            :subtasks="subtasks"
            :boardId="props.board.id"
            :states="props.states"
            :members="props.members"
            @selected="openTask"
          />
        </div>

        <Divider />

        <div class="mb-6">
          <div class="flex gap-2 items-center justify-between mb-2">
            <div class="text-lg font-semibold mb-2">Activity</div>
            <div>
              <RadioGroup
                v-model:value="selectedCommentType"
                @change="handleCommentTypeChange"
              >
                <Radio value="all">All</Radio>
                <Radio value="update">Updates</Radio>
                <Radio value="activity">Activity</Radio>
              </RadioGroup>
            </div>
          </div>

          <TaskCommentAddForm
            :boardId="props.board.id"
            :taskId="props.taskId"
            @added="addNewComment"
          />

          <TaskCommentList
            :boardId="props.board.id"
            :taskId="props.taskId"
            :comments="comments"
          />
        </div>
      </div>

      <div class="col-span-3">
        <TaskActionBar
          :isArchived="isArchived"
          :task="task"
          :board="props.board"
          :members="props.members"
          :priorities="props.priorities"
          :states="props.states"
          @update="updateTaskItem"
        />
      </div>
    </div>

    <!-- Subtask Add Form -->
    <Modal
      v-model:open="showSubtaskAddForm"
      title="Add subtask"
      :footer="null"
      centered
      destroyOnClose
      width="700px"
    >
      <SubTaskAddForm
        :task="task"
        :boardId="props.board.id"
        @created="addTaskToSubtask"
        :members="props.members"
        :priorities="props.priorities"
        :states="props.states"
      />
    </Modal>
  </div>
  <div v-else>
    <Skeleton />
  </div>
</template>

<style scoped></style>
