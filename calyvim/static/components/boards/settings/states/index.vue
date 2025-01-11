<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue'
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { onMounted, ref, h } from 'vue'
import {
  stateListAPI,
  stateSequenceUpdateAPI,
  stateDeleteAPI,
  stateUpdateAPI,
} from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'
import {
  CloseOutlined,
  EditOutlined,
  HolderOutlined,
  PlusOutlined,
} from '@ant-design/icons-vue'
import {
  Button,
  FormItem,
  Input,
  Textarea,
  Modal,
  Dropdown,
  message,
} from 'ant-design-vue'
import { VueDraggable } from 'vue-draggable-plus'
import StateAddForm from './state-add-form.vue'
import StateEditForm from './state-edit-form.vue'

const props = defineProps(['workspace', 'board', 'hasEditPermission'])

const states = ref([])
const loadStates = async () => {
  try {
    const { data } = await stateListAPI(props.board.id)
    states.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const selectedState = ref(null)
const openStateEditForm = (stateId) => {
  selectedState.value = stateId
}
const closeEditForm = () => {
  selectedState.value = null
}

const onUpdate = async (event) => {
  const updatedData = {}
  try {
    const state = states.value[event.newIndex]

    if (event.newIndex === 0 && states.value.length === 1) {
      // Empty
    } else if (event.newIndex === 0) {
      updatedData['nextState'] = states.value[event.newIndex + 1].id
    } else if (event.newIndex === states.value.length - 1) {
      updatedData['previousState'] = states.value[event.newIndex - 1].id
    } else {
      updatedData['nextState'] = states.value[event.newIndex + 1].id
      updatedData['previousState'] = states.value[event.newIndex - 1].id
    }

    const { data } = await stateSequenceUpdateAPI(
      props.board.id,
      state.id,
      updatedData
    )
    state.sequence = data.newSequence
  } catch (error) {
    handleResponseError(error)
  }
}

const updateState = async (stateId, values) => {
  try {
    const state = states.value.find((p) => p.id === stateId)
    const { data } = await stateUpdateAPI(props.board.id, stateId, values)
    notify('SUCCESS', data.detail)
    state.name = data.state.name
  } catch (error) {
    handleResponseError(error)
  } finally {
    closeEditForm()
  }
}

onMounted(() => {
  loadStates()
})

const showAddStateDropdown = ref(false)
const addState = (newState) => {
  states.value.push(newState)
  message.success(`New state ${newState.name} has been added.`)
  showAddStateDropdown.value = false
}

const deleteState = async (stateId) => {
  try {
    await stateDeleteAPI(props.board.id, stateId)
    states.value = states.value.filter((state) => state.id !== stateId)
    message.success('State got deleted')
  } catch (error) {}
}
</script>

<template>
  <BoardSettingsLayout
    :workspace="props.workspace"
    :board="props.board"
    page="boards"
    subPage="settings"
  >
    <div class="flex justify-between mb-2">
      <div class="text-lg">States</div>
      <div class="text-sm text-gray-500">
        Drag to update the order of states
      </div>
      <div>
        <Dropdown v-model:open="showAddStateDropdown" :trigger="['click']">
          <Button
            type="primary"
            :icon="h(PlusOutlined)"
            :disabled="!props.hasEditPermission"
            >Add state</Button
          >

          <template #overlay>
            <StateAddForm :boardId="props.board.id" @added="addState" />
          </template>
        </Dropdown>
      </div>
    </div>
    <div class="flex flex-col gap-2">
      <VueDraggable
        v-model="states"
        class="flex flex-col gap-1"
        @update="onUpdate"
      >
        <div
          v-for="state in states"
          class="w-full rounded overflow-hidden shadow bg-white py-3 my-1 px-2 border-solid border border-gray-200"
        >
          <div class="flex justify-between relative group">
            <div v-if="selectedState === state.id" class="w-full">
              <StateEditForm
                :boardId="props.board.id"
                :state="state"
                @close="closeEditForm"
                @update="updateState"
              />
            </div>
            <template v-else>
              <div class="flex items-center gap-1 cursor-pointer">
                <HolderOutlined />
                <div class="text-primary font-semibold">{{ state.name }}</div>
              </div>
              <div
                class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              >
                <Button
                  type="text"
                  :icon="h(EditOutlined)"
                  :disabled="!props.hasEditPermission"
                  @click="openStateEditForm(state.id)"
                  >Edit</Button
                >
                <Button
                  type="text"
                  :icon="h(CloseOutlined)"
                  danger
                  @click="deleteState(state.id)"
                  :disabled="!props.hasEditPermission"
                ></Button>
              </div>
            </template>
          </div>
        </div>
      </VueDraggable>
    </div>
  </BoardSettingsLayout>
</template>
