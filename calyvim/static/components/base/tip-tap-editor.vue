<script setup>
import { ref, onMounted, onBeforeUnmount, h } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { Button } from 'ant-design-vue'
import { Check, X } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'saved'])

const isEditorFocused = ref(false)
const isEditMode = ref(false) // New state to track edit mode

const editor = useEditor({
  content: props.modelValue,
  extensions: [StarterKit],
  editorProps: {
    attributes: {
      class:
        'prose prose-sm max-w-none focus:outline-none overflow-y-auto px-2 py-1',
    },
  },
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

const handleFocus = () => {
  isEditorFocused.value = true
  isEditMode.value = true
}

const handleBlur = (event) => {
  // Only update focus state, but keep edit mode active
  const isActionButton = event.relatedTarget?.closest('.editor-actions')
  const isEditorContainer = event.relatedTarget?.closest('.editor-container')

  if (!isEditorContainer && !isActionButton) {
    isEditorFocused.value = false
  }
}

const saveContent = () => {
  emit('saved', editor.value.getHTML())
  isEditorFocused.value = false
  isEditMode.value = false // Exit edit mode on save
}

const cancelEdit = () => {
  isEditorFocused.value = false
  isEditMode.value = false // Exit edit mode on cancel
}

onMounted(() => {
  editor.value.on('focus', handleFocus)
  editor.value.on('blur', handleBlur)
})

onBeforeUnmount(() => {
  editor.value.off('focus', handleFocus)
  editor.value.off('blur', handleBlur)
})

const toggleBold = () => editor.value.chain().focus().toggleBold().run()
const toggleItalic = () => editor.value.chain().focus().toggleItalic().run()
const toggleStrike = () => editor.value.chain().focus().toggleStrike().run()
const toggleCode = () => editor.value.chain().focus().toggleCode().run()
const toggleBulletList = () =>
  editor.value.chain().focus().toggleBulletList().run()
const toggleOrderedList = () =>
  editor.value.chain().focus().toggleOrderedList().run()
const toggleCodeBlock = () =>
  editor.value.chain().focus().toggleCodeBlock().run()
const toggleBlockquote = () =>
  editor.value.chain().focus().toggleBlockquote().run()

const actionButtons = [
  {
    icon: 'B',
    action: toggleBold,
    isActive: () => editor.value?.isActive('bold'),
  },
  {
    icon: 'I',
    action: toggleItalic,
    isActive: () => editor.value?.isActive('italic'),
  },
  {
    icon: 'S',
    action: toggleStrike,
    isActive: () => editor.value?.isActive('strike'),
  },
  {
    icon: '<>',
    action: toggleCode,
    isActive: () => editor.value?.isActive('code'),
  },
  {
    icon: '•',
    action: toggleBulletList,
    isActive: () => editor.value?.isActive('bulletList'),
  },
  {
    icon: '1.',
    action: toggleOrderedList,
    isActive: () => editor.value?.isActive('orderedList'),
  },
  {
    icon: '{ }',
    action: toggleCodeBlock,
    isActive: () => editor.value?.isActive('codeBlock'),
  },
  {
    icon: '"',
    action: toggleBlockquote,
    isActive: () => editor.value?.isActive('blockquote'),
  },
]
</script>

<template>
  <div class="editor-container border rounded-lg">
    <!-- Editor Actions -->
    <div
      v-show="isEditMode"
      class="editor-actions flex items-center gap-1 border-b p-1 bg-gray-50"
    >
      <Button
        size="small"
        type="text"
        v-for="(action, index) in actionButtons"
        :key="index"
        @mousedown.prevent="() => action.action()"
        :class="{ 'bg-gray-200': action.isActive() }"
      >
        {{ action.icon }}
      </Button>
    </div>

    <!-- Editor Content -->
    <div class="editor-content-wrapper" style="height: 200px; overflow-y: auto" :class="{ 'border-solid border-gray-200 rounded-sm mb-1': isEditMode }">
      <editor-content :editor="editor" />
    </div>

    <!-- Bottom Actions -->
    <div
      v-show="isEditMode"
      class="editor-actions flex justify-end gap-2 border-t p-"
    >
      <Button @click="cancelEdit" size="small" type="text">
        <template #icon>
          <X class="w-4 h-4 align-middle" />
        </template>
      </Button>

      <Button type="primary" @click="saveContent" size="small">
        <template #icon>
          <Check class="w-4 h-4 align-middle" />
        </template>
      </Button>
    </div>
  </div>
</template>

<style>
/* Minimal Tiptap Styles */
.ProseMirror {
  height: 100%;
  min-height: 100%;
}

.ProseMirror p {
  margin: 0;
}

/* Other basic styles */
.ProseMirror ul,
.ProseMirror ol {
  padding-left: 1rem;
}

.ProseMirror blockquote {
  border-left: 2px solid #ddd;
  padding-left: 0.5rem;
  margin-left: 0;
}

.ProseMirror code {
  background-color: #f1f1f1;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
}

.ProseMirror pre code {
  display: block;
  background-color: #2d2d2d;
  color: #fff;
  padding: 0.5rem;
}

/* Ensure content is scrollable */
.editor-content-wrapper {
  overflow-y: auto;
  position: relative;
}

.editor-content-wrapper .ProseMirror {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}
</style>
