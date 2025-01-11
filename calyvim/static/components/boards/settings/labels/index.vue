<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue'
import { CloseOutlined, PlusOutlined, TagFilled } from '@ant-design/icons-vue'
import { Button, List, ListItem, Form, FormItem, Input } from 'ant-design-vue'
import { h, onMounted, ref } from 'vue'
import { useNProgress } from '@vueuse/integrations/useNProgress'
import { labelListAPI, labelCreateAPI, labelDeleteAPI } from '@/utils/api'
import { handleResponseError, notify } from '@/utils/helpers'

const props = defineProps({
  workspace: {
    type: Object,
    required: true,
  },
  board: {
    type: Object,
    required: true,
  },
  hasEditPermission: {
    type: Boolean,
    required: true,
  },
})
const labels = ref([])

const { isLoading } = useNProgress(null, { minimum: 0.5 })

const openAddLabelForm = ref(false)
const showAddLabelForm = () => {
  openAddLabelForm.value = true
}
const closeAddLabelForm = () => {
  openAddLabelForm.value = false
}

const loadLabels = async () => {
  try {
    isLoading.value = true
    const { data } = await labelListAPI(props.board.id)
    labels.value = data.results
  } catch (error) {
    handleResponseError(error)
  } finally {
    isLoading.value = false
  }
}

const labelAddForm = ref({
  name: '',
  color: '#000000',
})

const onSubmit = async (values) => {
  try {
    const { data } = await labelCreateAPI(props.board.id, values)
    notify('SUCCESS', data.detail)
    labels.value = [data.label, ...labels.value]
    labelAddForm.value = {
      name: '',
      color: '#000000',
    }
    closeAddLabelForm()
  } catch (error) {
    handleResponseError(error)
  }
}

const deleteLabel = async (labelId) => {
  try {
    const { data } = await labelDeleteAPI(props.board.id, labelId)
    notify('DELETED', 'Label deleted', 'info')
    labels.value = labels.value.filter((label) => label.id !== labelId)
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(() => {
  loadLabels()
})
</script>

<template>
  <BoardSettingsLayout
    :workspace="props.workspace"
    :board="props.board"
    page="boards"
    subPage="settings"
  >
    <div class="flex justify-between items-center mb-2">
      <div class="font-semibold text-lg">Labels</div>
      <Button :icon="h(PlusOutlined)" type="primary" @click="showAddLabelForm"
        >Add label</Button
      >
    </div>

    <div>
      <Form
        :model="labelAddForm"
        @finish="onSubmit"
        v-if="openAddLabelForm"
        layout="inline"
      >
        <div class="flex gap-2 mx-3">
          <FormItem class="m-0 p-0" name="color" label="Color">
            <Input
              v-model:value="labelAddForm.color"
              placeholder="Label name"
              type="color"
            />
          </FormItem>
          <FormItem class="m-0 p-0" name="name">
            <Input v-model:value="labelAddForm.name" placeholder="Label name" />
          </FormItem>
          <FormItem class="m-0 p-0">
            <Button type="primary" html-type="submit">Add</Button>
          </FormItem>
        </div>
      </Form>
    </div>

    <List :dataSource="labels">
      <template #renderItem="{ item }">
        <ListItem class="group">
          <div class="w-full">
            <div class="flex items-center justify-between">
              <div>
                <TagFilled :style="{ color: item.color }" />
                <span class="ml-2 font-semibold">{{ item.name }}</span>
              </div>

              <div
                class="flex items-center gap-2 invisible group-hover:visible"
              >
                <Button size="small" type="text" @click="deleteLabel(item.id)">
                  <CloseOutlined @click="" class="text-xs text-red-400" />
                </Button>
              </div>
            </div>
          </div>
        </ListItem>
      </template>
    </List>
  </BoardSettingsLayout>
</template>
