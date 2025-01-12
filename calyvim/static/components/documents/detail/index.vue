<script setup>
import { blockListAPI } from '@/utils/api'
import DocumentLayout from '@/components/base/document-layout.vue'
import { onMounted, ref, nextTick } from 'vue'
import { Button, Textarea, Dropdown, Menu, MenuItem } from 'ant-design-vue'
import { DeleteIcon, EllipsisVertical, Heading1, Heading2, Heading3, Text, List, Trash2 } from 'lucide-vue-next'

const props = defineProps(['document', 'workspace'])

const blocks = ref([])
const document = ref(props.document)

const loadBlocks = async () => {
  const { data } = await blockListAPI(props.document.id)
  blocks.value = data.results
}

const textareaRefs = ref([])

const handleKeyDown = async (event, index) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    const newBlock = {
      id: crypto.randomUUID(),
      blockType: 'paragraph',
      properties: {
        text: '',
      },
    }

    console.log(newBlock)

    blocks.value.splice(index + 1, 0, newBlock)

    await nextTick()
    textareaRefs.value[index + 1]?.focus()
  } else if (
    event.key === 'Backspace' &&
    blocks.value[index].properties.text === '' &&
    blocks.value.length > 1
  ) {
    event.preventDefault()
    removeBlock(index)
    await nextTick()
    textareaRefs.value[index - 1]?.focus()
  }
}

const removeBlock = (index) => {
  if (blocks.value.length > 1) {
    blocks.value.splice(index, 1)
  }
}

onMounted(async () => {
  await loadBlocks()
  await textareaRefs.value[0]?.focus()
})
</script>

<template>
  <DocumentLayout
    :workspace="props.workspace"
    :document="props.document"
    page="documents"
    subPage="page"
  >
    <!-- Todo  -->
    <div class="max-w-4xl mx-auto p-8">
      <div class="space-y-2">
        <div
          v-for="(block, index) in blocks"
          :key="block.id"
          class="relative group"
        >
          <Textarea
            v-model:value="block.properties.text"
            :autoSize="{ minRows: 1 }"
            :bordered="false"
            class="block w-full resize-none bg-transparent hover:bg-gray-50 p-2 rounded focus:ring-2"
            :ref="
              (el) => {
                if (el) textareaRefs[index] = el
              }
            "
            @keydown="handleKeyDown($event, index)"
          />
          <div
            class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-8 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <Dropdown :trigger="['click']">
              <Button type="text" class="mr-1">
                <template #icon><EllipsisVertical class="h-3 w-3 align-middle" /></template>
              </Button>
              <template #overlay>
                <Menu>
                  <MenuItem>
                    <template #icon><Heading1 class="h-3 w-3 align-middle" /></template>
                    Heading 1
                  </MenuItem>
                  <MenuItem>
                    <template #icon><Heading2 class="h-3 w-3 align-middle" /></template>
                    Heading 2
                  </MenuItem>
                  <MenuItem>
                    <template #icon><Heading3 class="h-3 w-3 align-middle" /></template>
                    Heading 3
                  </MenuItem>
                  <Menu-divider />
                  <MenuItem>
                    <template #icon><Text class="h-3 w-3 align-middle" /></template>
                    Text
                  </MenuItem>
                  <MenuItem>
                    <template #icon><List class="h-3 w-3 align-middle" /></template>
                    Bullet List
                  </MenuItem>
                  <Menu-divider />
                  <MenuItem
                    @click="removeBlock(index)"
                    v-if="blocks.length > 1"
                  >
                    <template #icon><Trash2 class="h-3 w-3 align-middle" /></template>
                    Delete
                  </MenuItem>
                </Menu>
              </template>
            </Dropdown>
          </div>
        </div>
      </div>
    </div>
  </DocumentLayout>
</template>
