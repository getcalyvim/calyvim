import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', () => {
  const kanban = ref([])

  const states = ref([])
  const members = ref([])
  const priorities = ref([])
  const sprints = ref([])
  const estimates = ref([])
  const labels = ref([])

  const groupBy = ref(null)

  const assigneeFilters = ref([])
  const taskTypes = ref([])
  const priorityFilters = ref([])
  const labelFilters = ref([])
  const estimateFilters = ref([])
  const sprintFilters = ref([])

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

  const initializeEstimates = (estimatesData) => {
    estimates.value = estimatesData
  }

  const initializeLabels = (labelsData) => {
    labels.value = labelsData
  }

  const updateTask = (
    taskId,
    updatedData,
    groupByProperty = null,
    groupByPropertyId = null
  ) => {
    if (groupBy.value) {
      if (
        (groupByProperty && groupByProperty !== groupBy.value) ||
        (!groupByProperty && !groupByPropertyId)
      ) {
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

  const updateTaskPositionByGroup = (
    taskId,
    stateId,
    groupKey,
    updatedData
  ) => {
    kanban.value.forEach((item) => {
      item.states.forEach((state) => {
        const taskIndex = state.tasks.findIndex((task) => task.id === taskId)
        if (taskIndex !== -1) {
          const taskToMove = state.tasks.splice(taskIndex, 1)[0]
          console.log(taskToMove)
          kanban.value.forEach((item) => {
            if (item.groupKey === groupKey) {
              item.states.forEach((state) => {
                if (state.id === stateId) {
                  state.tasks.push({ ...taskToMove, ...updatedData })
                  state.tasks.sort((a, b) => a.sequence - b.sequence)
                }
              })
            }
          })
        }
      })
    })
  }

  const updateTaskPosition = (taskId, stateId, updatedData) => {
    kanban.value.forEach((item) => {
      const taskIndex = item.tasks.findIndex((task) => task.id === taskId)
      if (taskIndex !== -1) {
        const taskToMove = item.tasks.splice(taskIndex, 1)[0]

        kanban.value.forEach((item) => {
          if (item.id === stateId) {
            item.tasks.push({ ...taskToMove, ...updatedData })
            item.tasks.sort((a, b) => a.sequence - b.sequence)
          }
        })
      }
    })
  }

  const addTask = (task) => {
    if (!groupBy.value) {
      // No group by
      kanban.value.forEach((state) => {
        if (state.id === task.stateId) {
          state.tasks.push(task)
          state.tasks.sort((a, b) => a.sequence - b.sequence)
        }
      })

      return
    }

    // If Grouping is present
    if (task.assigneeId && groupBy.value === 'assignee') {
      kanban.value.forEach((item) => {
        if (item.groupKey === task.assigneeId) {
          item.states.forEach((state) => {
            if (state.id === task.stateId) {
              state.tasks.push(task)
              state.tasks.sort((a, b) => a.sequence - b.sequence)
            }
          })
        }
      })
    } else if (task.sprintId && groupBy.value === 'sprint') {
      kanban.value.forEach((item) => {
        if (item.groupKey === task.sprintId) {
          item.states.forEach((state) => {
            if (state.id === task.stateId) {
              state.tasks.push(task)
              state.tasks.sort((a, b) => a.sequence - b.sequence)
            }
          })
        }
      })
    } else if (task.priorityId && groupBy.value === 'priority') {
      kanban.value.forEach((item) => {
        if (item.groupKey === task.priorityId) {
          item.states.forEach((state) => {
            if (state.id === task.stateId) {
              state.tasks.push(task)
              state.tasks.sort((a, b) => a.sequence - b.sequence)
            }
          })
        }
      })
    } else if (groupBy.value === 'task_type') {
      kanban.value.forEach((item) => {
        if (item.groupKey === task.taskType) {
          item.states.forEach((state) => {
            if (state.id === task.stateId) {
              state.tasks.push(task)
              state.tasks.sort((a, b) => a.sequence - b.sequence)
            }
          })
        }
      })
    } else {
      // TODO: Handle to the last ungrouped section
      console.log('Skipping')
    }
  }

  const setActiveSprint = (sprintId) => {
    sprintFilters.value = [sprintId]
  }

  const clearFilters = () => {
    assigneeFilters.value = []
    taskTypes.value = []
    priorityFilters.value = []
    labelFilters.value = []
    estimateFilters.value = []
    sprintFilters.value = []
  }

  return {
    // State
    kanban,
    states,
    members,
    priorities,
    groupBy,
    sprints,
    estimates,
    labels,
    assigneeFilters,
    taskTypes,
    priorityFilters,
    labelFilters,
    estimateFilters,
    sprintFilters,

    // Actions
    initializeKanban,
    initializeStates,
    initializeMembers,
    initializePriorities,
    initializeGroupBy,
    initializeSprints,
    initializeEstimates,
    initializeLabels,
    updateTask,
    updateTaskPositionByGroup,
    updateTaskPosition,
    clearFilters,
    setActiveSprint,
    addTask,
  }
})
