<script setup>
import { Checkbox, CheckboxGroup, Tag } from 'ant-design-vue';
import { useBoardStore } from '@/stores/board';
import { TagTwoTone } from '@ant-design/icons-vue';
import { computed, ref } from 'vue';

const emit = defineEmits(['reload'])
const store = useBoardStore()

const showAllLabels = ref(false)

const visibleLabels = computed(() => {
    return showAllLabels.value ? store.labels : store.labels.slice(0, 5)
})

const toggleLabelVisibility = () => {
    showAllLabels.value = !showAllLabels.value
}
</script>

<template>
    <CheckboxGroup v-model:value="store.labelFilters" class="" @change="emit('reload')">
        <div class="flex flex-col gap-1">
            <div v-for="label in visibleLabels" :key="label.id" class="flex items-center gap-1">
                <Checkbox :value="label.id"></Checkbox>
                <Tag :bordered="false" >
                    <TagTwoTone :twoToneColor="label.color" />
                    {{ label.name }}
                </Tag>
            </div>
            <div v-if="store.labels.length > 5" class="mt-2">
                <a href="#" @click.prevent="toggleLabelVisibility">
                    {{ showAllLabels ? 'View less' : 'View more' }}
                </a>
            </div>
        </div>
    </CheckboxGroup>
</template>