import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', () => {
    const kanban = ref([])

    const states = ref([])
    const members = ref([])
    const priorities = ref([])

    const groupBy = ref(null)

    const initializeStates = (kanbanData) => {
        states.value = kanbanData
    }

    const initializeMembers = (membersData) => {
        members.value = membersData
    }

    const initializePriorities = (prioritiesData) => {
        priorities.value = prioritiesData
    }

    const initializeKanban = (kanbanData) => {
        kanban.value = kanbanData
    }

    const initializeGroupBy = (groupByData) => {
        groupBy.value = groupByData
    }
    
    return {
        // State
        kanban,
        states,
        members,
        priorities,
        groupBy,

        // Actions
        initializeKanban,
        initializeStates,
        initializeMembers,
        initializePriorities,
        initializeGroupBy,
    }
})