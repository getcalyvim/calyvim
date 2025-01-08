<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Button } from 'ant-design-vue'
import { h, onMounted, ref } from 'vue'
import {  } from '../../../utils/api/newslines'
import { handleResponseError } from '../../../utils/helpers'
import { Newspaper } from 'lucide-vue-next'
const props = defineProps(['workspace', 'currentUser'])

</script>

<template>
  <WorkspaceLayout
    :workspace="props.workspace"
    :currentUser="props.currentUser"
    page="documents"
  >
    <div class="flex justify-center items-center h-[90vh]">
      <div class="text-center mt-5">
        <Newspaper class="text-primary h-12 w-12" />
        <h2 class="text-xl font-bold">Documents</h2>
        <h2 class="text-lg font-semibold">
          This feature is currently being developed, we will be right back soon.
        </h2>
        <p class="text">
          Manage all your documents at one place.
        </p>
      </div>
    </div>
  </WorkspaceLayout>
</template>
