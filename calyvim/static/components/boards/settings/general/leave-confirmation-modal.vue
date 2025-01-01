<script setup>
import { Button, Input } from 'ant-design-vue'
import { computed, ref } from 'vue'
const props = defineProps(['board'])

const confirmName = ref('')

const disabled = computed(() => {
  return `boards/${props.board.name}` !== confirmName.value
})

const leaveBoard = () => {
  window.location.href = `/app/b/${props.board.id}/leave/`
}
</script>

<template>
  <div class="mb-2">
    Are you sure you want to leave this board? Leaving will remove your
    access to all its tasks and resources.
  </div>
  <div class="text-xs text-gray-400 mb-3">
    Note: This action is irreversible. To regain access, you will need an
    invitation from a workspace admin. If you have permission through teams, you
    will still have access to the board.
  </div>

  <div class="mb-7">
    <div class="mb-1">
      Please type <span class="font-bold">boards/{{ props.board.name }}</span> to
      confirm.
    </div>
    <Input v-model:value="confirmName" />
  </div>

  <Button danger class="w-full" :disabled="disabled" @click="leaveBoard"
    >I want to leave this board</Button
  >
</template>
