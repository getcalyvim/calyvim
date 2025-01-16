<script setup>
import { blockListAPI, blockOperationsAPI } from '@/utils/api'
import DocumentLayout from '@/components/base/document-layout.vue'
import { onMounted, ref, nextTick, computed } from 'vue'
import { Button, Dropdown, Menu, MenuItem } from 'ant-design-vue'
import {
  EllipsisVertical,
  Heading1,
  Heading2,
  Heading3,
  Text,
  List,
  Trash2,
} from 'lucide-vue-next'
import { debounce } from 'lodash'

const props = defineProps(['document', 'workspace'])

const blocks = ref([])
const blockOrder = computed(() => blocks.value.map((block) => block.id))
const document = ref(props.document)

const loadBlocks = async () => {
  const { data } = await blockListAPI(props.document.id)
  blocks.value = data.results
}

const textareaRefs = ref([])

const pendingUpdates = ref(new Map())

const handleKeyDown = async (event, index) => {
  if (event.key === 'ArrowUp') {
    if (index === 0) return

    event.preventDefault()
    const selection = window.getSelection()
    const currentPosition = selection.anchorOffset
    const prevDiv = textareaRefs.value[index - 1]

    // TODO: handle the case where the current block has newline

    prevDiv?.focus()
    const range = new Range()
    let textNode = prevDiv.firstChild
    if (!textNode) {
      textNode = document.createTextNode('')
      prevDiv.appendChild(textNode)
    }
    const position = Math.min(currentPosition, textNode.length)

    try {
      range.setStart(textNode, position)
      range.setEnd(textNode, position)
      selection.removeAllRanges()
      selection.addRange(range)
    } catch (error) {
      console.error('Range error:', error)
    }
  } else if (event.key === 'ArrowDown') {
    if (index >= blocks.value.length - 1) return

    event.preventDefault()
    const selection = window.getSelection()
    const currentPosition = selection.anchorOffset
    const nextDiv = textareaRefs.value[index + 1]

    // TODO: handle the case where the current block has newline

    nextDiv?.focus()
    const range = new Range()
    let textNode = nextDiv.firstChild
    if (!textNode) {
      textNode = document.createTextNode('')
      nextDiv.appendChild(textNode)
    }
    const position = Math.min(currentPosition, textNode.length)

    try {
      range.setStart(textNode, position)
      range.setEnd(textNode, position)
      selection.removeAllRanges()
      selection.addRange(range)
    } catch (error) {
      console.error('Range error:', error)
    }
  } else if (event.key === 'Enter') {
    if (event.shiftKey) {
      event.preventDefault()
      const selection = window.getSelection()
      const currentPosition = selection.anchorOffset
      const range = selection.getRangeAt(0)
      const textNode = range.startContainer

      const beforeText = textNode.textContent.slice(0, currentPosition)
      const afterText = textNode.textContent.slice(currentPosition)
      textNode.textContent = beforeText + '\n' + afterText

      range.setStart(textNode, currentPosition + 1)
      range.setEnd(textNode, currentPosition + 1)
      selection.removeAllRanges()
      selection.addRange(range)

      return
    }

    event.preventDefault()
    const newBlock = {
      id: crypto.randomUUID(),
      blockType: 'paragraph',
      properties: { text: '' },
    }

    blocks.value.splice(index + 1, 0, newBlock)
    await nextTick()
    textareaRefs.value[index + 1]?.focus()
    debouncedSave()
  } else if (
    event.key === 'Backspace' &&
    !event.target.textContent &&
    blocks.value.length > 1
  ) {
    event.preventDefault()
    removeBlock(index)
    await nextTick()
    textareaRefs.value[index - 1]?.focus()
  }
}

const handleInput = (event, block) => {
  block.properties.text = event.target.textContent
  saveBlockChanges(block.id, {
    properties: { text: event.target.textContent },
  })
}

const removeBlock = (index) => {
  if (blocks.value.length > 1) {
    blocks.value.splice(index, 1)
    debouncedSave()
  }
}

const debouncedSave = debounce(async () => {
  const hasChanges = pendingUpdates.value.size > 0

  if (!hasChanges) return

  const updatedData = { updates: {}, content: blockOrder.value }

  await pendingUpdates.value.forEach((value, key) => {
    if (blockOrder.value.includes(key)) {
      updatedData.updates[key] = value
    }
  })

  try {
    await blockOperationsAPI(document.value.id, updatedData)
    pendingUpdates.value = new Map()
  } catch (error) {
    console.error('Failed to save blocks:', error)
  }
}, 3000)

const saveBlockChanges = (id, payload) => {
  pendingUpdates.value.set(id, payload)
  debouncedSave()
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
    <div class="max-w-4xl mx-auto p-8">
      <div class="space-y-2">
        <div
          v-for="(block, index) in blocks"
          :key="block.id"
          class="relative group"
        >
          <div
            :ref="
              (el) => {
                if (el) textareaRefs[index] = el
              }
            "
            :contenteditable="true"
            class="block w-full min-h-[1.5em] bg-transparent hover:bg-gray-50 p-2 rounded focus:outline-none whitespace-pre-wrap"
            @input="(e) => handleInput(e, block)"
            @keydown="handleKeyDown($event, index)"
            v-text="block.properties.text"
          />
          <div
            class="absolute right-0 top-1/2 -translate-y-1/2 translate-x-8 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <Dropdown :trigger="['click']">
              <Button type="text" class="mr-1">
                <template #icon>
                  <EllipsisVertical class="h-3 w-3 align-middle" />
                </template>
              </Button>
              <template #overlay>
                <Menu>
                  <MenuItem>
                    <template #icon>
                      <Heading1 class="h-3 w-3 align-middle" />
                    </template>
                    Heading 1
                  </MenuItem>
                  <MenuItem>
                    <template #icon>
                      <Heading2 class="h-3 w-3 align-middle" />
                    </template>
                    Heading 2
                  </MenuItem>
                  <MenuItem>
                    <template #icon>
                      <Heading3 class="h-3 w-3 align-middle" />
                    </template>
                    Heading 3
                  </MenuItem>
                  <Menu-divider />
                  <MenuItem>
                    <template #icon>
                      <Text class="h-3 w-3 align-middle" />
                    </template>
                    Text
                  </MenuItem>
                  <MenuItem>
                    <template #icon>
                      <List class="h-3 w-3 align-middle" />
                    </template>
                    Bullet List
                  </MenuItem>
                  <Menu-divider />
                  <MenuItem
                    @click="removeBlock(index)"
                    v-if="blocks.length > 1"
                  >
                    <template #icon>
                      <Trash2 class="h-3 w-3 align-middle" />
                    </template>
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
