<script setup>
import { Button, Input } from 'ant-design-vue'
import { computed, ref } from 'vue'
const props = defineProps(['board'])

const confirmName = ref('')

const disabled = computed(() => {
  return `boards/${props.board.name}` !== confirmName.value
})

const deleteBoard = () => {
  window.location.href = `/boards/${props.board.id}/delete/`
}
</script>

<template>
  <div class="mb-2">
    Are you sure you want to delete this board? Deleting will clear all its
    tasks and resources data.
  </div>
  <div class="text-xs text-gray-400 mb-3">
    Note: This action is irreversible
  </div>

  <div class="mb-7">
    <div class="mb-1">
      Please type
      <span class="font-bold">boards/{{ props.board.name }}</span> to confirm.
    </div>
    <Input v-model:value="confirmName" />
  </div>

  <Button danger class="w-full" :disabled="disabled" @click="deleteBoard"
    >I want to delete this board</Button
  >
</template>
