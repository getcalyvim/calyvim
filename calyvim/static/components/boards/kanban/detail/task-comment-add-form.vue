<script setup>
import { SaveOutlined } from '@ant-design/icons-vue'
import { Button, Form, FormItem, message, Textarea, Input } from 'ant-design-vue'
import { h, ref } from 'vue'
import { handleResponseError } from '@/utils/helpers';
import { taskCommentsCreateAPI } from '@/utils/api';

const props = defineProps(['boardId', 'taskId'])
const emit = defineEmits(['added'])

const form = ref({
  content: '',
})
const formRef = ref()

const onFinish = async (values) => {
    try {
        const { data } = await taskCommentsCreateAPI(props.boardId, props.taskId, values)
        formRef.value.resetFields()

        emit('added', data)

        message.success('Comment added')
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
  <Form
    layout="horizontal"
    :model="form"
    name="task-comment-add"
    @finish="onFinish"
    hide-required-mark
    ref="formRef"
  >
    <div class="flex justify-between gap-4">
      <FormItem name="content" :rules="[{ message: 'Comment is requuired', required: true }]" class="w-full">
        <Input v-model:value="form.content" placeholder="Add a comment.." />
      </FormItem>
      <FormItem>
        <Button type="primary" html-type="submit" :icon="h(SaveOutlined)"> Comment</Button>
      </FormItem>
    </div>
  </Form>
</template>
