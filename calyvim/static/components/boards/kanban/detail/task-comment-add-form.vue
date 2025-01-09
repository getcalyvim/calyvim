<script setup>
import {
  Button,
  Form,
  FormItem,
  Input,
} from 'ant-design-vue'
import { h, ref } from 'vue'
import { handleResponseError, notify } from '@/utils/helpers'
import { taskCommentsCreateAPI } from '@/utils/api'
import { MessageSquarePlus } from 'lucide-vue-next'

const props = defineProps(['boardId', 'taskId'])
const emit = defineEmits(['added'])

const form = ref({
  content: '',
})
const formRef = ref()

const onFinish = async (values) => {
  try {
    const { data } = await taskCommentsCreateAPI(
      props.boardId,
      props.taskId,
      values
    )
    formRef.value.resetFields()

    emit('added', data.comment)
    notify('ADDED', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <div class="grid grid-cols-12 gap-4">
    <div class="col-span-9">
      <Form
        layout="horizontal"
        :model="form"
        name="task-comment-add"
        @finish="onFinish"
        hide-required-mark
        ref="formRef"
      >
        <div class="flex justify-between gap-4">
          <FormItem
            name="content"
            :rules="[{ message: 'Comment is requuired', required: true }]"
            class="w-full p-0"
          >
            <Input v-model:value="form.content" placeholder="Add a comment.." />
          </FormItem>
          <FormItem>
            <Button
              type="primary"
              html-type="submit"
              :icon="
                h(MessageSquarePlus, { class: 'w-4 h-4 align-middle mr-2' })
              "
            >
              Comment</Button
            >
          </FormItem>
        </div>
      </Form>
    </div>
  </div>
</template>
