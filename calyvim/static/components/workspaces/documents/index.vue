<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Button, Card } from 'ant-design-vue'
import { h, onMounted, ref } from 'vue'
import { documentListAPI } from '../../../utils/api'
import { handleResponseError } from '../../../utils/helpers'
import { File, EllipsisVertical } from 'lucide-vue-next'
import { useNProgress } from '@vueuse/integrations/useNProgress'
const { isLoading } = useNProgress(null, { minimum: '0.5' })

const props = defineProps(['workspace', 'currentUser'])

const documents = ref([])

const loadDocuments = async () => {
  try {
    const { data } = await documentListAPI(props.workspace.id)
    documents.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

const openDocument = (documentId) => {
  window.location.href = `/documents/${documentId}`
}

onMounted(() => {
  loadDocuments()
})
</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :currentUser="props.currentUser"
    page="documents"
  >
    <div class="py-2 px-4">
      <div class="flex justify-between items-center">
        <div class="text-lg font-semibold">Documents</div>
        <Button type="primary" :icon="h(PlusOutlined)">Create document</Button>
      </div>
      <div class="grid grid-cols-4">
        <Card size="small" v-for="document in documents" :key="document.id" class="cursor-pointer" @click="openDocument(document.id)">
          <div class="flex justify-between items-center">
            <div class="flex gap-2 items-center">
              <File class="w-4 h-4 text-primary" />
              <div class="text-md font-semibold">{{ document.name }}</div>
            </div>
            <Button type="text" size="small">
              <template #icon>
                <EllipsisVertical class="w-3 h-3 align-middle" />
              </template>
            </Button>
          </div>
          <div class="text-sm text-gray-500">{{ document.description }}</div>
        </Card>
      </div>
    </div>
  </WorkspaceLayout>
</template>
