<script setup>
import { Avatar, Button, Card, InputSearch } from 'ant-design-vue';
import { computed, h, ref } from 'vue';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import { boardTeamPermissionCreateAPI, workspaceTeamSearchAPI } from '@/utils/api';
import { PlusOutlined } from '@ant-design/icons-vue';

const props = defineProps(['workspaceId', 'teams', 'boardId'])
const emit = defineEmits(['teamAdded'])

const existingTeamIds = computed(() => props.teams.map(team => team.id))

const searchValue = ref('')
const searchTeams = ref([])
const onSearch = async (value) => {
    if (!value) return

    try {
        const { data } = await workspaceTeamSearchAPI(props.workspaceId, value)
        searchTeams.value = data
    } catch (error) {
        handleResponseError(error)
    }
}

const createBoardTeamPermission = async (teamId) => {
    try {
        const postData = {
            teamId: teamId,
            role: 'collaborator'
        }

        const { data } = await boardTeamPermissionCreateAPI(props.boardId, postData)

        emit('teamAdded', data)
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <InputSearch v-model:value="searchValue" @search="onSearch" class="mb-2" placeholder="Search teams" />
    <div v-if="searchTeams.length > 0" class="text-xs mb-1">Search results ...</div>
    <Card size="small w-full mb-1" v-for="member in searchTeams" :key="member.id">
        <div class="flex justify-between items-center">
            <div class="flex gap-2 items-center">
                <Avatar :src="!!member.avatar ? member.avatar : generateAvatar(member.name, 10)" shape="square" />
                <div>{{ member.name }}</div>
            </div>

            <div>
                <Button v-if="existingTeamIds.includes(member.id)" disabled type="text">Already present</Button>
                <Button v-else type="text" :icon="h(PlusOutlined)"
                    @click="createBoardTeamPermission(member.id)">Add</Button>
            </div>
        </div>
    </Card>
</template>