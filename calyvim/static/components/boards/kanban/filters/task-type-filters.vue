<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useBoardStore } from '@/stores/board';
import TaskTypeIcon from '@/components/icons/task-type-icon.vue';

const emit = defineEmits(['reload'])
const store = useBoardStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.taskTypes" class="" @change="emit('reload')">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-1">
                <Checkbox value="issue"></Checkbox>
                <TaskTypeIcon taskType="issue" />
                <div>Issue</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="feature"></Checkbox>
                <TaskTypeIcon taskType="feature" />
                <div>Feature</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="story"></Checkbox>
                <TaskTypeIcon taskType="story" />
                <div>Story</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="bug"></Checkbox>
                <TaskTypeIcon taskType="bug" />
                <div>Bug</div>
            </div>
        </div>
    </CheckboxGroup>
</template>