import { client } from './client'
export const taskUpdateAPI = (boardId, taskId, data) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}`, data)

export const taskListAPI = (boardId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks`, {
    params: filters,
  })

export const taskDetailAPI = (boardId, taskId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks/${taskId}`, {
    params: {
      ...filters,
    },
  })

export const taskListKanbanAPI = (boardId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks/kanban`, {
    params: filters,
  })

export const taskArchiveAPI = (boardId, taskId) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}/archive`)

export const taskRestoreAPI = (boardId, taskId) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}/restore`)

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

export const taskUpdateSequenceAPI = (boardId, taskId, data) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}/update-sequence`, data)

export const taskShareLinkAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/share-link`)

export const taskAddLabelAPI = (boardId, taskId, labelId) =>
  client.patch(
    `/boards/${boardId}/tasks/${taskId}/add-label`,
    {},
    {
      params: {
        labelId,
      },
    }
  )

export const taskRemoveLabelAPI = (boardId, taskId, labelId) =>
  client.patch(
    `/boards/${boardId}/tasks/${taskId}/remove-label`,
    {},
    {
      params: {
        labelId,
      },
    }
  )

export const taskBulkUpdateAPI = (boardId, data) =>
  client.patch(`/boards/${boardId}/tasks/bulk-update`, data)
