<script setup>
import { Form, FormItem, Input, Button } from 'ant-design-vue'

const props = defineProps(['boardId', 'priority'])
const emit = defineEmits(['update', 'close'])

</script>

<template>
  <Form :model="props.priority" @finish="(values) => emit('update', props.priority.id, values)" hideRequiredMark>
    <div class="flex items-center justify-between">
      <FormItem name="name" required class="m-0 p-0">
        <Input v-model:value="props.priority.name" />
      </FormItem>
      <FormItem class="m-0 p-0">
        <div class="flex items-center gap-2">
            <Button html-type="submit" type="primary" size="small">Submit</Button>
            <Button size="small" @click="emit('close')">Cancel</Button>
        </div>
      </FormItem>
    </div>
  </Form>
</template>
