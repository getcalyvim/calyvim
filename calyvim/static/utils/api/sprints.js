import { client } from './client'

export const sprintListAPI = (boardId) =>
  client.get(`/boards/${boardId}/sprints`)

export const sprintCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/sprints`, data)

export const sprintActivateAPI = (boardId, sprintId) =>
  client.patch(`/boards/${boardId}/sprints/${sprintId}/activate`)

export const sprintDeleteAPI = (boardId, sprintId) =>
  client.delete(`/boards/${boardId}/sprints/${sprintId}`)

export const sprintArchiveAPI = (boardId, sprintId) =>
  client.patch(`/boards/${boardId}/sprints/${sprintId}/archive`)

export const sprintBurndownAPI = (boardId, sprintId) => {
  return client.get(`/boards/${boardId}/sprints/${sprintId}/burndown`)
}
