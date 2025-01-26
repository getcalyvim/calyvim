<script setup>
import {
  Form,
  FormItem,
  Input,
  Button,
  Select,
  SelectOption,
} from 'ant-design-vue'

const props = defineProps(['boardId', 'state'])
const emit = defineEmits(['update', 'close'])
</script>

<template>
  <Form
    :model="props.state"
    @finish="(values) => emit('update', props.state.id, values)"
    hideRequiredMark
  >
    <div class="flex items-center justify-between">
      <div class="flex gap-6">
        <FormItem name="name" required class="m-0 p-0">
          <Input v-model:value="props.state.name" />
        </FormItem>
        <FormItem name="category" size="small" class="m-0 p-0 w-48" required label="Category">
          <Select v-model:value="props.state.category">
            <SelectOption value="open">Open</SelectOption>
            <SelectOption value="active">Active</SelectOption>
            <SelectOption value="completed">Completed</SelectOption>
          </Select>
        </FormItem>
      </div>
      <FormItem class="m-0 p-0">
        <div class="flex items-center gap-2">
          <Button html-type="submit" type="primary" size="small">Submit</Button>
          <Button size="small" @click="emit('close')">Cancel</Button>
        </div>
      </FormItem>
    </div>
  </Form>
</template>
