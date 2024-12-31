<script setup>
import { Skeleton } from 'ant-design-vue'

const props = defineProps(['states'])
</script>

<template>
  <div class="flex space-x-3">
    <div
      v-for="state in props.states"
      :key="state.id"
      class="rounded-lg w-[21rem] flex-shrink-0 py-2 flex flex-col gap-2"
    >
      <Skeleton
        v-for="n in Math.floor(Math.random() * 4) + 1"
        :key="n"
        active
      />
    </div>
  </div>
</template>
