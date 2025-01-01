<script setup>
import BoardLayout from '@/components/base/board-layout.vue'
import {
  BarsOutlined,
  HddOutlined,
  NodeExpandOutlined,
  ProjectOutlined,
  TagsOutlined,
  TeamOutlined,
} from '@ant-design/icons-vue'
import {
  Layout,
  LayoutContent,
  LayoutSider,
  Menu,
  MenuItem,
} from 'ant-design-vue'
import { ref } from 'vue'

const props = defineProps(['workspace', 'board', 'page'])
const collapsed = ref(false)
const selectedKeys = ref([props.page])

const changePage = (event) => {
  if (event.key === 'general') {
    window.location.href = `/app/b/${props.board.id}/settings`
  } else {
    window.location.href = `/app/b/${props.board.id}/settings/${event.key}/`
  }
}
</script>

<template>
  <BoardLayout
    :workspace="props.workspace"
    :board="props.board"
    page="settings"
  >
    <div class="container mx-auto">
      <Layout v-model:collapsed="collapsed" :trigger="null" collapsible>
        <LayoutSider>
          <Menu v-model:selectedKeys="selectedKeys" mode="inline">
            <MenuItem key="general">
              <a
                :href="`/app/b/${props.board.id}/settings`"
                class="no-underline text-inherit hover:no-underline hover:text-inherit"
                :class="{
                  'text-primary hover:text-primary':
                    selectedKeys[0] === 'general',
                }"
              >
                <BarsOutlined />
                <span>General</span>
              </a>
            </MenuItem>

            <MenuItem key="collaborators">
              <a
                :href="`/app/b/${props.board.id}/settings/collaborators`"
                class="no-underline text-inherit hover:no-underline hover:text-inherit"
                :class="{
                  'text-primary hover:text-primary':
                    selectedKeys[0] === 'collaborators',
                }"
              >
                <TeamOutlined />
                <span>Collaborators</span>
              </a>
            </MenuItem>

            <MenuItem key="states">
              <a
                :href="`/app/b/${props.board.id}/settings/states`"
                class="no-underline text-inherit hover:no-underline hover:text-inherit"
                :class="{
                  'text-primary hover:text-primary':
                    selectedKeys[0] === 'states',
                }"
              >
                <HddOutlined />
                <span>States</span>
              </a>
            </MenuItem>

            <MenuItem key="priorities">
              <a
                :href="`/app/b/${props.board.id}/settings/priorities`"
                class="no-underline text-inherit hover:no-underline hover:text-inherit"
                :class="{
                  'text-primary hover:text-primary':
                    selectedKeys[0] === 'priorities',
                }"
              >
                <NodeExpandOutlined />
                <span>Priorities</span>
              </a>
            </MenuItem>

            <MenuItem key="labels" disabled>
              <a
                :href="`/app/b/${props.board.id}/settings/labels`"
                class="no-underline text-inherit hover:no-underline hover:text-inherit"
                :class="{
                  'text-primary hover:text-primary':
                    selectedKeys[0] === 'labels',
                }"
              >
                <TagsOutlined />
                <span>Labels</span>
              </a>
            </MenuItem>
          </Menu>
        </LayoutSider>

        <Layout>
          <LayoutContent>
            <slot></slot>
          </LayoutContent>
        </Layout>
      </Layout>
    </div>
  </BoardLayout>
</template>

<style scoped>
.ant-layout-sider {
  min-height: 100vh;
  background: #fff;
  border-right: 1px solid #a9a9a9;
}

.ant-layout-content {
  padding: 18px;
  background: #fff;
}

.ant-layout-header {
  background: #fff;
  padding: 0;
  border-bottom: 1px solid gray;
}
</style>
