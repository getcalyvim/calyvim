import { client } from './client'

export const boardListAPI = (workspaceId) =>
  client.get(`/boards`, {
    params: {
      workspaceId,
    },
  })
export const boardCreateAPI = (data) => client.post(`/boards`, data)
export const boardDetailAPI = (boardId) => client.get(`/boards/${boardId}`)
export const boardUpdateAPI = (boardId, data) =>
  client.patch(`/boards/${boardId}`, data)
export const boardMembersListAPI = (boardId) =>
  client.get(`/boards/${boardId}/members`)

export const taskCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/tasks`, data)



export const boardStatsAPI = (workspaceId) =>
  client.get(`/boards/stats`, {
    params: {
      workspaceId,
    },
  })

export const boardTemplatesAPI = (workspaceId) =>
  client.get(`/boards/templates`, {
    params: {
      workspaceId,
    },
  })

export const boardMetadataAPI = (boardId) =>
  client.get(`/boards/${boardId}/metadata`)
