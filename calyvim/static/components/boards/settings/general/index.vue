<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue'
import { h, onMounted, ref } from 'vue'
import {
  Avatar,
  Form,
  FormItem,
  Input,
  Textarea,
  Upload,
  Button,
  message,
  Divider,
  Collapse,
  CollapsePanel,
  Modal,
} from 'ant-design-vue'
import { boardDetailAPI, boardUpdateAPI } from '@/utils/api'
import {
  CloseOutlined,
  DeleteOutlined,
  LogoutOutlined,
  PlusOutlined,
  SaveOutlined,
  EditOutlined,
} from '@ant-design/icons-vue'
import { generateAvatar, uploadRequestHandler } from '@/utils/helpers'
import { handleResponseError } from '@/utils/helpers'
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import LeaveConfirmationModal from '@/components/boards/settings/general/leave-confirmation-modal.vue'
import DeleteConfirmationModal from '@/components/boards/settings/general/delete-confirmation-modal.vue'

const props = defineProps(['workspace', 'board', 'hasEditPermission'])
const activeKey = ref([''])

const boardForm = ref({
  name: '',
  description: '',
  cover: null,
  coverSrc: null,
  logo: null,
  logoSrc: null,
  taskPrefix: '',
  slug: '',
})

const onFinish = async (values) => {
  try {
    await boardUpdateAPI(props.board.id, values)
    message.success('Board details updated successfully!')
  } catch (error) {
    handleResponseError(error)
  }
}

const handleCoverUpload = async (options) => {
  const { fileKey, fileSrc } = await uploadRequestHandler(
    options,
    'Board',
    'cover'
  )
  boardForm.value.cover = fileKey
  boardForm.value.coverSrc = fileSrc
}

const handleLogoUpload = async (options) => {
  const { fileKey, fileSrc } = await uploadRequestHandler(
    options,
    'Board',
    'logo'
  )
  boardForm.value.logo = fileKey
  boardForm.value.logoSrc = fileSrc
}

const removeCover = () => {
  boardForm.value.cover = null
  boardForm.value.coverSrc = null
}

const removeLogo = () => {
  boardForm.value.logo = null
  boardForm.value.logoSrc = null
}

const fetchBoard = async () => {
  const { data } = await boardDetailAPI(props.board.id)
  boardForm.value = {
    name: data.name,
    description: data.description,
    cover: data.cover,
    coverSrc: data.coverSrc,
    taskPrefix: data.taskPrefix,
    slug: data.slug,
    logo: data.logo,
    logoSrc: data.logoSrc,
  }
}

const openLeaveConfirmationModal = ref(false)
const showLeaveConfirmationModal = () => {
  openLeaveConfirmationModal.value = true
}

const openDeleteConfirmationModal = ref(false)
const showDeleteConfirmationModal = () => {
  openDeleteConfirmationModal.value = true
}

onMounted(() => {
  fetchBoard()
})
</script>

<template>
  <BoardSettingsLayout
    :workspace="props.workspace"
    :board="props.board"
    page="boards"
    subPage="settings"
  >
    <div class="mx-auto px-4">
      <div class="max-w-3xl mx-auto">
        <Form
          :model="boardForm"
          layout="vertical"
          @finish="onFinish"
          :disabled="!props.hasEditPermission"
        >
          <div class="relative w-full mb-4">
            <div
              class="w-full h-32 md:h-40 lg:h-48 bg-gray-100 overflow-hidden rounded-lg"
            >
              <div
                class="w-full h-full bg-gradient-to-r from-gray-400 to-primary"
              >
                <img
                  v-if="!!boardForm.coverSrc"
                  :src="boardForm.coverSrc"
                  class="w-full h-full object-cover"
                  alt="Banner"
                />
              </div>
            </div>

            <div class="absolute bottom-4 left-4 z-10">
              <div
                class="w-20 h-20 rounded-lg shadow-lg flex items-center justify-center relative"
              >
                <Avatar
                  :src="
                    !!boardForm.logoSrc
                      ? boardForm.logoSrc
                      : generateAvatar(boardForm.name, 12)
                  "
                  shape="square"
                  :size="84"
                />

                <div
                  class="absolute inset-0 flex items-center justify-center gap-1 opacity-0 hover:opacity-100 bg-white/20 transition-opacity duration-200"
                >
                  <FormItem name="logo" class="p-0 m-0">
                    <Upload
                      :multiple="false"
                      name="file"
                      :customRequest="handleLogoUpload"
                      :show-upload-list="false"
                    >
                      <Button
                        type="text"
                        class="flex items-center justify-center"
                      >
                        <template #icon><EditOutlined /></template>
                      </Button>
                    </Upload>
                  </FormItem>
                  <Button
                    type="text"
                    class="flex items-center justify-center"
                    @click="removeLogo"
                  >
                    <template #icon><DeleteOutlined /></template>
                  </Button>
                </div>
              </div>
            </div>

            <div class="absolute bottom-4 right-4 z-10 flex space-x-0">
              <div>
                <FormItem name="cover" class="p-0 m-0">
                  <Upload
                    :multiple="false"
                    name="file"
                    :customRequest="handleCoverUpload"
                    :show-upload-list="false"
                  >
                    <Button
                      type="text"
                      class="flex items-center justify-center"
                    >
                      <template #icon><EditOutlined /></template>
                    </Button>
                  </Upload>
                </FormItem>
              </div>

              <Button
                type="text"
                class="flex items-center justify-center"
                @click="removeCover"
              >
                <template #icon><DeleteOutlined /></template>
              </Button>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <FormItem label="Name" name="name">
              <Input v-model:value="boardForm.name" />
            </FormItem>

            <FormItem label="Board ID" name="slug">
              <Input v-model:value="boardForm.slug" />
            </FormItem>
          </div>

          <FormItem label="Description" name="description">
            <Textarea v-model:value="boardForm.description" :rows="4" />
          </FormItem>

          <div class="grid grid-cols-2 gap-4">
            <FormItem label="Task prefix" name="taskPrefix">
              <Input v-model:value="boardForm.taskPrefix" />
            </FormItem>
          </div>

          <div class="flex justify-end">
            <FormItem>
              <Button type="primary" html-type="submit" :icon="h(SaveOutlined)"
                >Update board</Button
              >
            </FormItem>
          </div>
        </Form>

        <Divider />
        <Collapse v-model:activeKey="activeKey" ghost>
          <CollapsePanel key="leave" header="Leave board">
            <div class="text-gray-500">
              Please proceed with caution. Leaving this board will result in the
              loss of access to all associated tasks. If you wish to rejoin in
              the future, you will need to be added by an existing member.
              Ensure you are certain of this decision before proceeding.
            </div>
            <Button
              danger
              class="mt-2"
              :icon="h(LogoutOutlined)"
              @click="showLeaveConfirmationModal"
              >Leave board</Button
            >
          </CollapsePanel>

          <CollapsePanel
            key="delete"
            header="Delete board"
            :collapsible="hasEditPermission ? 'header' : 'disabled'"
          >
            <div class="text-gray-500">
              Please proceed with extreme caution. Deleting this workspace will
              permanently erase all associated data, tasks. Members will lose
              access immediately, and the workspace cannot be recovered. If you
              are certain of this decision, please confirm before proceeding.
            </div>
            <Button
              danger
              class="mt-2"
              :icon="h(DeleteOutlined)"
              type="primary"
              @click="showDeleteConfirmationModal"
              >Delete board</Button
            >
          </CollapsePanel>
        </Collapse>
      </div>
    </div>
  </BoardSettingsLayout>

  <Modal
    v-model:open="openLeaveConfirmationModal"
    title="Leave confirmation"
    centered
  >
    <LeaveConfirmationModal :board="props.board" />

    <template #footer>
      <!-- <Button @click="openLeaveConfirmationModal = false">Cancel</Button> -->
    </template>
  </Modal>

  <Modal
    v-model:open="openDeleteConfirmationModal"
    title="Delete confirmation"
    centered
  >
    <DeleteConfirmationModal :board="props.board" />

    <template #footer>
      <!-- <Button @click="openLeaveConfirmationModal = false">Cancel</Button> -->
    </template>
  </Modal>
</template>
