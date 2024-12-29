import { client } from './client'

export const priorityListAPI = (boardId) =>
  client.get(`/boards/${boardId}/priorities`)

export const priorityUpdateAPI = (boardId, priorityId, data) =>
  client.patch(`/boards/${boardId}/priorities/${priorityId}`, data)

export const priorityCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/priorities`, data)

export const priorityDeleteAPI = (boardId, priorityId) =>
  client.delete(`/boards/${boardId}/priorities/${priorityId}`)
