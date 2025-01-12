import { client } from './client'

export const blockListAPI = (documentId) => client.get(`/documents/${documentId}/blocks`)
