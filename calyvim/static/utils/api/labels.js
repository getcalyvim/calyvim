import { client } from './client'

export const labelListAPI = (boardId) => client.get(`/boards/${boardId}/labels`)

export const labelCreateAPI = (boardId, data) => client.post(`/boards/${boardId}/labels`, data)

export const labelDeleteAPI = (boardId, labelId) => client.delete(`/boards/${boardId}/labels/${labelId}`)