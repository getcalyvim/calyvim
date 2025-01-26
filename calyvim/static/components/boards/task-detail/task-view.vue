<script setup>
import { h, onMounted, ref } from 'vue'
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
} from 'ant-design-vue'
import {
  EllipsisOutlined,
  ShareAltOutlined,
  SyncOutlined,
  PlusOutlined,
  SwitcherOutlined,
  LinkOutlined,
  CheckSquareOutlined,
  FileOutlined,
  ArrowLeftOutlined,
} from '@ant-design/icons-vue'
import { Package, Undo2 } from 'lucide-vue-next'
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
import TaskActionBar from './task-action-bar.vue'
import TaskCommentAddForm from './task-comment-add-form.vue'
import TaskAttachmentList from './task-attachment-list.vue'
import SubTaskList from './sub-task-list.vue'
import TipTapEditor from '@/components/base/tip-tap-editor.vue'
import TaskLabels from './task-labels.vue'

// API imports
import {
  taskCommentsAPI,
  taskAttachmentsDeleteAPI,
  taskDetailAPI,
  taskUpdateAPI,
  taskAttachmentsCreateAPI,
  taskAttachmentsListAPI,
  taskListAPI,
  taskArchiveAPI,
  taskRestoreAPI,
  taskShareLinkAPI,
  taskAddLabelAPI,
  taskRemoveLabelAPI,
} from '@/utils/api'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'

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
  sprints: {
    type: Array,
    default: () => [],
  },
  labels: {
    type: Array,
    default: () => [],
  },
  estimates: {
    type: Array,
    default: () => [], 
  }
})

const currentTaskId = ref(props.taskId)
const emit = defineEmits(['update', 'selected', 'remove'])

// State
const loading = ref(false)
const updateLoading = ref(false)
const selectedCommentType = ref('update')
const task = ref(null)
const comments = ref([])
const attachments = ref([])
const subtasks = ref([])
const showSubtaskAddForm = ref(false)
const isArchived = ref(false)

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
  loadComments(currentTaskId.value)
}

// Attachments Management
const createAttachment = async (options) => {
  const { fileKey, fileSrc } = await uploadRequestHandler(
    options,
    'TaskAttachment',
    'attachment',
    localStorage.getItem('workspaceCode')
  )

  try {
    const { data } = await taskAttachmentsCreateAPI(
      props.board.id,
      currentTaskId.value,
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
      currentTaskId.value,
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

const updateDescription = () => {
  updateTaskItem({ description: task.value.description })
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

const addTaskToSubtask = (data) => {
  closeSubtaskAddForm()
  subtasks.value.push(data)
}

// Loading and Initialization
const loadTaskDetails = async (taskId) => {
  try {
    loading.value = true
    const { data } = await taskDetailAPI(props.board.id, taskId, {
      include: ['attachments', 'subtasks', 'comments'],
    })
    task.value = {
      ...data.task,
    }
    attachments.value = data.attachments
    comments.value = data.comments
    subtasks.value = data.subtasks
  } catch (error) {
    handleResponseError(error)
  } finally {
    loading.value = false
  }
}

// Lifecycle Hooks
onMounted(() => {
  loadTaskDetails(currentTaskId.value)
})

const updateTaskv2 = async (updatedData) => {
  try {
    const { data } = await taskUpdateAPI(
      props.board.id,
      currentTaskId.value,
      updatedData
    )
    notify('UPDATED', data.detail)
    logComment(data.log)
  } catch (error) {
    handleResponseError(error)
  }
}

const updateTaskItem = async (updatedData) => {
  await updateTaskv2(updatedData)
  await emit('update', currentTaskId.value, updatedData)
}

const openTask = async (taskId) => {
  emit('selected', taskId)
  currentTaskId.value = taskId
  await loadTaskDetails(taskId)
}

const shareCopyToClipboard = async () => {
  try {
    const { data } = await taskShareLinkAPI(props.board.id, currentTaskId.value)
    await navigator.clipboard.writeText(data.shareLink)
    message.success('Link copied to clipboard')
  } catch (error) {
    handleResponseError(error)
  }
}

const addLabel = async (labelId) => {
  try {
    const label = props.labels.find((label) => label.id === labelId)
    task.value.labels.push(label)
    const { data } = await taskAddLabelAPI(
      props.board.id,
      currentTaskId.value,
      labelId
    )
    notify('ADDED', data.detail)
    await emit('update', currentTaskId.value, { labels: task.value.labels })
    logComment(data.log)
  } catch (error) {
    handleResponseError(error)
  }
}

const deleteLabel = async (labelId) => {
  try {
    task.value.labels = task.value.labels.filter(
      (label) => label.id !== labelId
    )
    const { data } = await taskRemoveLabelAPI(
      props.board.id,
      currentTaskId.value,
      labelId
    )
    notify('REMOVED', data.detail)
    await emit('update', currentTaskId.value, { labels: task.value.labels })
    logComment(data.log)
  } catch (error) {
    handleResponseError(error)
  }
}

const archive = async () => {
  try {
    const { data } = await taskArchiveAPI(props.board.id, currentTaskId.value)
    notify('ARCHIVED', data.detail)
    isArchived.value = true
    logComment(data.log)
    emit('remove', currentTaskId.value)
  } catch (error) {
    handleResponseError(error)
  }
}

const restore = async () => {
  try {
    const { data } = await taskRestoreAPI(props.board.id, currentTaskId.value)
    notify('RESTORED', data.detail)
    isArchived.value = false
    logComment(data.log)

    // TODO: Emit event to restore task in parent component
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <div v-if="!!task && !loading" class="flex flex-col h-full">
    <!-- Info Banner -->
    <div
      class="bg-gray-200 p-2 rounded font-semibold flex justify-between"
      v-if="isArchived"
    >
      <div class="flex items-center gap-2">
        <Package class="w-4 h-4" />
        <div>This task has been archived.</div>
      </div>

      <Button type="text" size="small" class="flex gap-1 items-center" @click="restore">
        <Undo2 class="w-4 h-4" />
        <div>Undo</div>
      </Button>
    </div>

    <!-- Fixed Header Section -->
    <div class="flex-none px-1 pt-4 mb-2">
      <div
        v-if="!!task.parentId"
        class="cursor-pointer mb-2"
        @click="openTask(task.parentId)"
      >
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
          <Button
            :icon="h(ShareAltOutlined)"
            type="text"
            @click="shareCopyToClipboard"
            >Share</Button
          >
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

    <!-- Scrollable Content Section -->
    <div class="flex-1 overflow-y-auto px-1">
      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-9">
          <div class="mb-3">
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

          <!-- Label -->
          <TaskLabels
            :task="task"
            :labels="props.labels"
            @addLabel="addLabel"
            @deleteLabel="deleteLabel"
          />

          <div class="text-lg font-semibold">Description</div>
          <div>
            <TipTapEditor
              v-model="task.description"
              @saved="updateDescription"
            />
          </div>

          <div class="mb-4">
            <TaskAttachmentList
              :boardId="props.board.id"
              :taskId="currentTaskId"
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
              :estimates="props.estimates"
              @selected="openTask"
            />
          </div>

          <Divider />

          <div class="mb-4">
            <div class="flex gap-2 items-center justify-between mb-2">
              <div class="text-lg font-semibold">Activity</div>
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

            <TaskCommentList
              :boardId="props.board.id"
              :taskId="currentTaskId"
              :comments="comments"
            />
          </div>

          <div class="mb-24">
            <!-- Added padding bottom for comment form -->
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
            :sprints="props.sprints"
            :labels="props.labels"
            :estimates="props.estimates"
            @update="updateTaskItem"
            @archive="archive"
          />
        </div>
      </div>
    </div>

    <!-- Fixed Comment Form at Bottom -->
    <div class="flex-none bg-white border-t px-1">
      <TaskCommentAddForm
        :boardId="props.board.id"
        :taskId="currentTaskId"
        @added="addNewComment"
      />
    </div>

    <!-- Modal remains outside scrollable area -->
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

<style scoped>
.h-full {
  height: 100%;
  max-height: 100vh;
}

.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}
</style>
