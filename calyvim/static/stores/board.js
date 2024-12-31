import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', () => {
  const kanban = ref([])

  const states = ref([])
  const members = ref([])
  const priorities = ref([])
  const sprints = ref([])

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

  const initializeSprints = (sprintsData) => {
    sprints.value = sprintsData
  }

  const updateTask = (
    taskId,
    updatedData,
    groupByProperty = null,
    groupByPropertyId = null
  ) => {
    if (groupBy.value) {
      if (groupByProperty && groupByProperty !== groupBy.value) {
        kanban.value.forEach((item) => {
          item.states.forEach((state) => {
            const task = state.tasks.find((task) => task.id === taskId)
            if (task) {
              Object.assign(task, updatedData)
            }
          })
        })
      } else {
        let taskToMove = null
        kanban.value.forEach((item) => {
          item.states.forEach((state) => {
            const taskIndex = state.tasks.findIndex(
              (task) => task.id === taskId
            )
            if (taskIndex !== -1) {
              taskToMove = state.tasks.splice(taskIndex, 1)[0]
            }
          })
        })

        if (taskToMove && groupByPropertyId) {
          kanban.value.forEach((item) => {
            if (item.groupKey === groupByPropertyId) {
              item.states.forEach((state) => {
                if (state.id === taskToMove.stateId) {
                  state.tasks.push({ ...taskToMove, ...updatedData })
                  state.tasks.sort((a, b) => a.sequence - b.sequence)
                }
              })
            }
          })
        }
      }
    } else {
      kanban.value.forEach((item) => {
        const task = item.tasks.find((task) => task.id === taskId)
        if (task) {
          Object.assign(task, updatedData)
        }
      })
    }
  }

  return {
    // State
    kanban,
    states,
    members,
    priorities,
    groupBy,
    sprints,

    // Actions
    initializeKanban,
    initializeStates,
    initializeMembers,
    initializePriorities,
    initializeGroupBy,
    initializeSprints,
    updateTask,
  }
})
