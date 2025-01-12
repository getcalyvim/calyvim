import { client } from './client'

export const blockListAPI = (documentId) =>
  client.get(`/documents/${documentId}/blocks`)

export const blockOperationsAPI = (documentId, operations) =>
  client.post(`/documents/${documentId}/blocks/operations`, operations)
