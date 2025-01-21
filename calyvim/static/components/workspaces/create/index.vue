<script setup>
import BaseLayout from '@/components/base/base-layout.vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import {
  Button,
  Form,
  FormItem,
  Input,
  Textarea,
  Select,
  SelectOption,
  Avatar,
  Checkbox,
} from 'ant-design-vue'
import { computed, h, ref, watch } from 'vue'
import { workspaceCreareAPI } from '@/utils/api'
import { handleResponseError, generateAvatar, slugify } from '@/utils/helpers'
import Logo from '@/assets/logo.png'

const props = defineProps({
  baseUrl: {
    type: String,
    required: true,
  },
  availableDomain: {
    type: String,
    default: null,
  },
})

const createForm = ref({
  name: '',
  description: '',
  orgSize: null,
  autoAssignMembership: false,
})

const onFinish = async (values) => {
  try {
    if (!!props.availableDomain) {
      values['autoAssignDomain'] = props.availableDomain
    }

    const { data } = await workspaceCreareAPI(values)
    window.location.href = `/${data.slug}/boards`
  } catch (error) {
    handleResponseError(error)
  }
}

const currentUser = computed(() => {
  return JSON.parse(localStorage.getItem('currentUser'))
})

const redirectToHome = () => {
  window.location.href = ''
}

const logoutUser = () => {
  localStorage.removeItem('currentUser')
  window.location.href = '/accounts/logout'
}
</script>

<template>
  <BaseLayout>
    <div
      class="h-screen flex overflow-hidden bg-gradient-to-br from-violet-50 via-purple-50 to-violet-100 relative"
    >
      <!-- Background with checkboxes and more visible shapes -->
      <div class="absolute inset-0">
        <!-- Original pattern -->
        <svg class="w-full h-full opacity-50" viewBox="0 0 60 60">
          <defs>
            <pattern
              id="pattern"
              x="0"
              y="0"
              width="60"
              height="60"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M36 34a8 8 0 100-16 8 8 0 000 16z"
                fill="#7D52E9"
                fill-opacity="0.05"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#pattern)" />
        </svg>

        <!-- Checkbox pattern -->
        <div
          class="absolute inset-0 opacity-[0.04]"
          style="
            background-image: linear-gradient(
                to right,
                #7d52e9 1px,
                transparent 1px
              ),
              linear-gradient(to bottom, #7d52e9 1px, transparent 1px);
            background-size: 20px 20px;
          "
        ></div>

        <!-- Small checkbox dots at intersections -->
        <div class="absolute inset-0 opacity-[0.03]">
          <svg class="w-full h-full" viewBox="0 0 20 20">
            <defs>
              <pattern
                id="dots"
                x="0"
                y="0"
                width="20"
                height="20"
                patternUnits="userSpaceOnUse"
              >
                <circle cx="1" cy="1" r="1" fill="#7D52E9" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#dots)" />
          </svg>
        </div>

        <!-- Decorative shapes with increased visibility -->
        <div
          class="absolute top-0 right-0 w-96 h-96 bg-[#7D52E9] rounded-full mix-blend-multiply filter blur-2xl opacity-[0.12] -translate-y-1/4 translate-x-1/4"
        ></div>
        <div
          class="absolute bottom-0 left-0 w-96 h-96 bg-[#7D52E9] rounded-full mix-blend-multiply filter blur-2xl opacity-[0.12] translate-y-1/4 -translate-x-1/4"
        ></div>

        <!-- Additional geometric shapes with increased visibility -->
        <div
          class="absolute top-1/4 left-1/3 w-32 h-32 bg-[#7D52E9] opacity-[0.06] rotate-45"
        ></div>
        <div
          class="absolute bottom-1/3 right-1/4 w-40 h-40 rounded-lg bg-[#7D52E9] opacity-[0.06] -rotate-12"
        ></div>
        <div
          class="absolute top-2/3 left-1/4 w-24 h-24 rounded-full bg-[#7D52E9] opacity-[0.06]"
        ></div>
      </div>

      <!-- Left side with branding -->
      <div
        class="w-1/2 hidden lg:flex flex-col items-center justify-center p-12 relative overflow-hidden"
      >
        <div class="max-w-md">
          <!-- Logo -->
          <img :src="Logo" alt="Calyvim" class="h-10 mb-4" />
          <h2 class="text-4xl font-bold mb-4 text-gray-900">
            Welcome to Calyvim
          </h2>
          <p class="text-lg text-gray-600">
            Create, collaborate, and manage your projects in one place. Get
            started by setting up your workspace.
          </p>
        </div>
      </div>

      <!-- Right side - form and user info -->
      <div
        class="w-full lg:w-1/2 p-8 relative flex flex-col justify-center overflow-y-auto"
      >
        <!-- User info and logout in top right corner -->
        <div class="absolute top-4 right-4 flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <div class="text-right">
              <div class="text-sm font-medium text-gray-900">
                {{ currentUser?.firstName }} {{ currentUser?.lastName }}
              </div>
              <div class="text-xs text-gray-500">{{ currentUser?.email }}</div>
              <div class="mt-1">
                <a
                  class="text-xs text-[#7D52E9] hover:text-[#6941C6] cursor-pointer underline underline-offset-2"
                  @click="logoutUser"
                  >Logout</a
                >
              </div>
            </div>
            <Avatar
              :src="
                currentUser?.avatar
                  ? currentUser.avatarSrc
                  : generateAvatar(currentUser?.firstName)
              "
              class="border-2 border-[#7D52E9]/10"
              alt="Profile"
            />
          </div>
        </div>

        <!-- Form -->
        <div class="max-w-md mx-auto w-full bg-white p-8 rounded-xl shadow-sm">
          <h1 class="text-2xl font-bold mb-6 text-gray-900">
            Create your workspace
          </h1>

          <Form :model="createForm" layout="vertical" @finish="onFinish">
            <FormItem
              label="Workspace Name"
              name="name"
              extra="Workspace name can be the name of your organization, company, etc."
            >
              <Input v-model:value="createForm.name" />
            </FormItem>

            <FormItem label="Organization Size" name="org_size">
              <Select v-model:value="createForm.orgSize">
                <SelectOption value="1">Just myself</SelectOption>
                <SelectOption value="0-10">0 - 10</SelectOption>
                <SelectOption value="11-50">11 - 50</SelectOption>
                <SelectOption value="51-200">51 - 200</SelectOption>
                <SelectOption value="201-500">201 - 500</SelectOption>
              </Select>
            </FormItem>

            <FormItem label="Workspace Description" name="description">
              <Textarea v-model:value="createForm.description" :rows="4" />
            </FormItem>

            <FormItem
              v-if="props.availableDomain"
              name="autoAssignMembership"
              help="You can toggle this setting later in your workspace settings."
            >
              <Checkbox v-model:checked="createForm.autoAssignMembership">
                Auto assign members as collaborators who register with the
                domain <strong>{{ props.availableDomain }}</strong
                >.
              </Checkbox>
            </FormItem>

            <div class="flex justify-end mt-3">
              <FormItem>
                <div class="flex gap-3">
                  <Button @click="redirectToHome">Go back</Button>
                  <Button
                    type="primary"
                    :icon="h(PlusOutlined)"
                    html-type="submit"
                    class="bg-[#7D52E9]"
                  >
                    Create
                  </Button>
                </div>
              </FormItem>
            </div>
          </Form>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>
