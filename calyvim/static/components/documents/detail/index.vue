<script setup>
import { documentListAPI } from '../../../utils/api'
import DocumentLayout from '../../base/document-layout.vue';

const props = defineProps(['document', 'workspace'])
</script>

<template>
    <DocumentLayout :workspace="props.workspace" :document="props.document" page="documents">
        <!-- Todo  -->
    </DocumentLayout>
</template>