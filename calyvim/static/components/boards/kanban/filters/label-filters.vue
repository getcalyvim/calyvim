<script setup>
import { Checkbox, CheckboxGroup, Tag } from 'ant-design-vue';
import { useBoardStore } from '@/stores/board';
import { TagTwoTone } from '@ant-design/icons-vue';

const emit = defineEmits(['reload'])
const store = useBoardStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.labelFilters" class="" @change="emit('reload')">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2" v-for="label in store.labels" :key="label.id">
                <Checkbox :value="label.id"></Checkbox>
                <div>
                    <TagTwoTone :two-tone-color="label.color" />
                    <span class="ml-2">
                        {{ label.name }}
                    </span>
                </div>
            </div>
        </div>
    </CheckboxGroup>
</template>