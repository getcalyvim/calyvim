<script setup>
import AccountsLayout from '@/components/base/accounts-layout.vue'
import { h, onMounted, ref } from 'vue'
import {
  Button,
  Form,
  FormItem,
  Input,
  InputPassword,
  message,
} from 'ant-design-vue'
import { GithubOutlined, GoogleOutlined } from '@ant-design/icons-vue'
import { accountsLoginAPI, accountsAuthenticateAPI } from '@/utils/api'
import GoogleOauthButton from './google-oauth-button.vue'
import BaseSpinner from '../base/base-spinner.vue'
import { handleResponseError } from '@/utils/helpers'

const props = defineProps({
  session: {
    type: Object,
    default: null,
  },
  hasGoogleOauth: {
    type: Boolean,
    default: false,
  },
  hasGithubOauth: {
    type: Boolean,
    default: false,
  },
})

const loginForm = ref({
  email: '',
  password: '',
})

const isSubmitting = ref(false)
const loading = ref(true)

const onFinish = async (values) => {
  try {
    isSubmitting.value = true
    const { data } = await accountsLoginAPI(values)
    localStorage.setItem('currentUser', JSON.stringify(data.user))
    window.location.href = `/`
  } catch (error) {
    handleResponseError(error)
  } finally {
    isSubmitting.value = false
  }
}

const authenticate = async (session) => {
  try {
    const { data } = await accountsAuthenticateAPI(session)
    localStorage.setItem('currentUser', JSON.stringify(data.user))
    window.location.href = `/`
    loading.value = false
  } catch (error) {
    handleResponseError(error)
    loading.value = false
  }
}

onMounted(async () => {
  if (!!props.session) {
    await authenticate(props.session)
  } else {
    loading.value = false
  }
})
</script>

<template>
  <AccountsLayout>
    <template v-if="loading">
      <div class="h-96 flex items-center justify-center">
        <BaseSpinner />
      </div>
    </template>
    <template v-else>
      <div class="flex items-center justify-center mb-4">
        <h1 class="text-2xl font-bold">Log In</h1>
      </div>

      <Form
        layout="vertical"
        :model="loginForm"
        name="loginForm"
        @finish="onFinish"
        hide-required-mark
      >
        <FormItem
          label="Email"
          name="email"
          :rules="[{ required: true, message: 'Please input your email!' }]"
        >
          <Input
            v-model:value="loginForm.email"
            placeholder="alison@company.com"
          />
        </FormItem>

        <FormItem
          label="Password"
          name="password"
          :rules="[
            { required: true, message: 'Please input a strong password!' },
          ]"
        >
          <template #extra>
            <a class="text-primary hover:text-primary" href="/accounts/reset/"
              >Forgot Password?</a
            >
          </template>
          <InputPassword
            v-model:value="loginForm.password"
            placeholder="***********"
          />
        </FormItem>

        <FormItem>
          <Button
            :loading="isSubmitting"
            type="primary"
            class="w-full"
            html-type="submit"
            >Log in</Button
          >
        </FormItem>
      </Form>

      <p class="mt-4 text-center text-sm text-gray-600">
        Don't have an account?
        <a href="/accounts/register/" class="font-medium text-primary"
          >Create an account</a
        >
      </p>

      <div class="mt-2">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm mb-2" v-if="hasGithubOauth || hasGoogleOauth">
            <span class="px-2 bg-white text-gray-500">Or</span>
          </div>
        </div>

        <div class="flex justify-center" v-if="hasGoogleOauth">
          <GoogleOauthButton />
        </div>
      </div>
    </template>
  </AccountsLayout>
</template>

<style scoped></style>
