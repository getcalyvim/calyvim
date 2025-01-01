<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Button } from 'ant-design-vue'
import { h, onMounted, ref } from 'vue'
import { newslineListAPI } from '../../../utils/api/newslines'
import { handleResponseError } from '../../../utils/helpers'
import { Newspaper } from 'lucide-vue-next'
const props = defineProps(['workspace', 'currentUser'])

const newslines = ref([])

const loadNewslines = async () => {
  try {
    const { data } = await newslineListAPI(props.workspace.id)
    newslines.value = data
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(() => {
  loadNewslines()
})
</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :currentUser="props.currentUser"
    page="newslines"
  >
    <div class="flex justify-center items-center h-[90vh]">
      <div class="text-center mt-5">
        <Newspaper class="text-primary h-12 w-12" />
        <h2 class="text-xl font-bold">Newslines</h2>
        <h2 class="text-lg font-semibold">
          This feature is currently being developed, we will be right back soon.
        </h2>
        <p class="text">
          This feature is like a notice board for your organization. This helps
          you share messages across your organization, teams, and your people.
        </p>
      </div>
    </div>
  </WorkspaceLayout>
</template>
