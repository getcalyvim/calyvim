import { client } from './client'

export const documentListAPI = (workspaceId) =>
  client.get(`/documents`, {
    params: {
      workspaceId,
    },
  })
