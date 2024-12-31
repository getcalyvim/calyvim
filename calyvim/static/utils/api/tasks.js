import { client } from './client'
export const taskUpdateAPI = (boardId, taskId, data) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}`, data)

export const taskListAPI = (boardId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks`, {
    params: filters,
  })

export const taskListKanbanAPI = (boardId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks/kanban`, {
    params: filters,
  })

export const taskArchiveApi = (boardId, taskId) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}/archive`)

export const taskCommentsAPI = (boardId, taskId, commentType = 'all') =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments`, {
    params: {
      commentType,
    },
  })

export const taskCommentsCreateAPI = (boardId, taskId, data) =>
  client.post(`/boards/${boardId}/tasks/${taskId}/comments`, data)

export const taskCommentsLastAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments/last`)

export const taskAttachmentsCreateAPI = (boardId, taskId, data) =>
  client.post(`/boards/${boardId}/tasks/${taskId}/attachments`, data)

export const taskAttachmentsListAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/attachments`)

export const taskAttachmentsDeleteAPI = (boardId, taskId, attachmentId) =>
  client.delete(
    `/boards/${boardId}/tasks/${taskId}/attachments/${attachmentId}`
  )

export const taskBulkStateUpdateAPI = (boardId, stateId, taskIds) =>
  client.patch(
    `/boards/${boardId}/tasks/state`,
    { taskIds },
    {
      params: {
        stateId,
      },
    }
  )
