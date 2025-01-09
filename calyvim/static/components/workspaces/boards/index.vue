<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { Card, Button, Modal } from 'ant-design-vue'
import { ref, onMounted, h } from 'vue'
import { boardListAPI } from '@/utils/api'
import dayjs from 'dayjs'
import { PlusOutlined } from '@ant-design/icons-vue'
import BoardNewModal from './board-new-modal.vue'
import { handleResponseError } from '@/utils/helpers'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import { CalendarCog } from 'lucide-vue-next'

const props = defineProps(['workspace', 'currentUser'])
const { isLoading } = useNProgress(null, { minimum: '0.5' })

const boards = ref([])
const fetchBoards = async () => {
  try {
    const { data } = await boardListAPI(props.workspace.id)
    boards.value = data
  } catch (err) {
    handleResponseError(err)
  } finally {
  }
}

const redirectToBoard = (board) => {
  window.location.href = `/boards/${board.id}/`
}

const openNewBoardModal = ref(false)
const showNewBoardModal = () => {
  openNewBoardModal.value = true
}
const closeNewBoardModal = () => {
  openNewBoardModal.value = false
}

onMounted(() => {
  fetchBoards()
})
</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :currentUser="props.currentUser"
    page="boards"
  >
    <div class="p-4" v-if="!isLoading">
      <div class="flex justify-between items-center">
        <div class="text-2xl font-semibold mb-3">Boards</div>
        <Button
          v-if="boards.length > 0"
          class=""
          type="primary"
          :icon="h(PlusOutlined)"
          @click="showNewBoardModal"
          >New board</Button
        >
      </div>
      <div class="grid grid-cols-3 gap-3" v-if="boards.length > 0">
        <Card
          v-for="board in boards"
          :key="board.id"
          size="small"
          @click="redirectToBoard(board)"
          class="cursor-pointer hover:border-solid hover:border-1 hover:border-primary"
          :style="{
            backgroundImage: board.cover
              ? `url(${board.cover})`
              : 'linear-gradient(to right, #F3F4F6, #ffffff)',
          }"
        >
          <div class="font-bold">{{ board.name }}</div>
          <div class="text-xs text-gray-500">
            Created on {{ dayjs(board.createdAt).format('MMMM D, YYYY') }}
          </div>
          <div class="text-sm">{{ board.description }}</div>
          <img
            v-if="board.logo"
            :src="board.logo"
            alt="Board Logo"
            class="w-10 h-10 mt-2 rounded"
          />
        </Card>
      </div>
      <div v-else class="flex justify-center items-center h-[70vh]">
        <div class="flex flex-col items-center gap-4">
          <CalendarCog class="mx-auto h-16 w-16 text-primary" />
          <div class="text-gray-500">
            You haven't created any boards yet. Get started by clicking on
            Create new board.
          </div>
          <Button
            type="primary"
            @click="showNewBoardModal"
            :icon="h(PlusOutlined)"
            >Create a new Board</Button
          >
        </div>
      </div>
    </div>
    <Modal v-model:open="openNewBoardModal" title="New board">
      <template #footer>
        <Button @click="closeNewBoardModal">Cancel</Button>
      </template>
      <BoardNewModal :workspace="props.workspace"></BoardNewModal>
    </Modal>
  </WorkspaceLayout>
</template>
