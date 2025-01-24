<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import { Button } from 'ant-design-vue'
import {
  Bold,
  Italic,
  Strikethrough,
  List,
  ListOrdered,
  Quote,
  Heading1,
  Heading2,
  Heading3,
  Code,
  Minus,
  Trash2,
  Check,
  X,
  Save,
} from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Type something...',
  },
})

const emit = defineEmits(['update:modelValue', 'saved'])

const isEditorFocused = ref(false)
const isEditMode = ref(false)

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Placeholder.configure({
      placeholder: props.placeholder, // Set the placeholder from props
    }),
  ],
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
  const isActionButton = event.relatedTarget?.closest('.editor-actions')
  const isEditorContainer = event.relatedTarget?.closest('.editor-container')

  if (!isEditorContainer && !isActionButton) {
    isEditorFocused.value = false
  }
}

const saveContent = () => {
  emit('saved', editor.value.getHTML())
  isEditorFocused.value = false
  isEditMode.value = false
}

const cancelEdit = () => {
  isEditorFocused.value = false
  isEditMode.value = false
}

onMounted(() => {
  editor.value.on('focus', handleFocus)
  editor.value.on('blur', handleBlur)
})

onBeforeUnmount(() => {
  editor.value.off('focus', handleFocus)
  editor.value.off('blur', handleBlur)
})

const actionButtons = [
  {
    icon: Bold,
    action: () => editor.value.chain().focus().toggleBold().run(),
    isActive: () => editor.value?.isActive('bold'),
  },
  {
    icon: Italic,
    action: () => editor.value.chain().focus().toggleItalic().run(),
    isActive: () => editor.value?.isActive('italic'),
  },
  {
    icon: Strikethrough,
    action: () => editor.value.chain().focus().toggleStrike().run(),
    isActive: () => editor.value?.isActive('strike'),
  },
  {
    icon: List,
    action: () => editor.value.chain().focus().toggleBulletList().run(),
    isActive: () => editor.value?.isActive('bulletList'),
  },
  {
    icon: ListOrdered,
    action: () => editor.value.chain().focus().toggleOrderedList().run(),
    isActive: () => editor.value?.isActive('orderedList'),
  },
  {
    icon: Quote,
    action: () => editor.value.chain().focus().toggleBlockquote().run(),
    isActive: () => editor.value?.isActive('blockquote'),
  },
  {
    icon: Heading1,
    action: () =>
      editor.value.chain().focus().toggleHeading({ level: 1 }).run(),
    isActive: () => editor.value?.isActive('heading', { level: 1 }),
  },
  {
    icon: Heading2,
    action: () =>
      editor.value.chain().focus().toggleHeading({ level: 2 }).run(),
    isActive: () => editor.value?.isActive('heading', { level: 2 }),
  },
  {
    icon: Heading3,
    action: () =>
      editor.value.chain().focus().toggleHeading({ level: 3 }).run(),
    isActive: () => editor.value?.isActive('heading', { level: 3 }),
  },
  {
    icon: Code,
    action: () => editor.value.chain().focus().toggleCode().run(),
    isActive: () => editor.value?.isActive('code'),
  },
  {
    icon: Minus,
    action: () => editor.value.chain().focus().setHorizontalRule().run(),
    isActive: () => false,
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
        <component :is="action.icon" class="w-4 h-4 align-middle" />
      </Button>
    </div>

    <!-- Editor Content -->
    <div
      class="editor-content-wrapper border-solid border-gray-200 rounded mb-1"
      style="height: 200px; overflow-y: auto"
    >
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

      <Button
        type="primary"
        @click="saveContent"
        size="small"
        class="flex items-center gap-1"
      >
        <Save class="w-3 h-3" />
        <span>Save</span>
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

.tiptap p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}
</style>
