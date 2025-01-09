<template>
    <div class="relative w-full border rounded-md">
      <!-- Default Description -->
      <div v-if="!isEditing" class="p-2" @click="enableEditing">
        <p class="text-gray-500 italic">{{ description }}</p>
      </div>
  
      <!-- Editor -->
      <div v-else class="p-2">
        <!-- Action Buttons -->
        <div class="flex items-center justify-between mb-2">
          <div class="flex gap-2">
            <button @click="applyAction('bold')" class="action-btn">
              <BoldOutlined />
            </button>
            <button @click="applyAction('italic')" class="action-btn">
              <ItalicOutlined />
            </button>
            <button @click="applyAction('code')" class="action-btn">
              <CodeOutlined />
            </button>
          </div>
          <!-- Tick and Cross Buttons -->
          <div class="flex gap-2">
            <button @click="confirm" class="action-btn text-green-500">
              <CheckOutlined />
            </button>
            <button @click="cancel" class="action-btn text-red-500">
              <CloseOutlined />
            </button>
          </div>
        </div>
  
        <!-- Content Editable Area -->
        <div
          ref="contentEditable"
          class="overflow-y-auto border rounded-md p-1"
          :style="{ height: height, padding: '0.5rem' }"
          contenteditable
          @input="updateContent"
        ></div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { BoldOutlined, CheckOutlined, CloseOutlined, ItalicOutlined, CodeOutlined } from "@ant-design/icons-vue";
  
  const props = defineProps({
    height: {
      type: String,
      default: "200px",
    },
    description: {
      type: String,
      default: "Click to edit...",
    },
    modelValue: {
      type: String,
      default: "",
    },
  });
  
  const emit = defineEmits(["update:modelValue", "confirm", "cancel"]);
  
  const isEditing = ref(false);
  const contentEditable = ref(null);
  
  const enableEditing = () => {
    isEditing.value = true;
    contentEditable.value.innerHTML = props.modelValue;
  };
  
  const updateContent = () => {
    emit("update:modelValue", contentEditable.value.innerHTML);
  };
  
  const applyAction = (action) => {
    document.execCommand(action, false, null);
  };
  
  const confirm = () => {
    emit("confirm", contentEditable.value.innerHTML);
    isEditing.value = false;
  };
  
  const cancel = () => {
    emit("cancel");
    isEditing.value = false;
  };
  </script>
  
  <style scoped>
  .action-btn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.25rem;
  }
  .action-btn:hover {
    background-color: #f3f4f6;
  }
  </style>
  