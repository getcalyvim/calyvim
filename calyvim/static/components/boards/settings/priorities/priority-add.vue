<script setup>
import { Form, FormItem, Button, Input, Card } from 'ant-design-vue'
import { h, ref } from 'vue'

import { handleResponseError } from '@/utils/helpers'
import { priorityCreateAPI } from '@/utils/api'
import { PlusOutlined } from '@ant-design/icons-vue'

const props = defineProps(['boardId'])
const emit = defineEmits(['created'])

const addForm = ref({
  name: '',
})
const formRef = ref(null)

const onSubmit = async (values) => {
  try {
    const { data } = await priorityCreateAPI(props.boardId, values)
    formRef.value.resetFields()
    emit('created', data.priority)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <Card class="w-72" size="small">
    <Form :model="addForm" @finish="onSubmit" layout="vertical" hideRequiredMark ref="formRef">
      <FormItem label="Priority name" name="name" required help="Name of the priority should be unique. You can edit it later.">
        <Input v-model:value="addForm.name" />
      </FormItem>
      <FormItem class="flex justify-end">
        <div class="flex gap-2">
            <Button>Reset fields</Button>
            <Button html-type="submit" type="primary" :icon="h(PlusOutlined)">Create</Button>
        </div>
      </FormItem>
    </Form>
  </Card>
</template>
