<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useBoardStore } from '@/stores/board';
import { FlagOutlined } from '@ant-design/icons-vue';

const emit = defineEmits(['reload'])
const store = useBoardStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.priorityFilters" class="" @change="emit('reload')">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2" v-for="priority in store.priorities" :key="priority.id">
                <Checkbox :value="priority.id"></Checkbox>
                <div>
                    <FlagOutlined class="text-primary" />
                    <span class="ml-2">{{ priority.name }}</span>
                </div>
            </div>
        </div>
    </CheckboxGroup>
</template>