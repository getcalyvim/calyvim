import { client, http } from './client'

export const blockListAPI = (documentId) =>
  client.get(`/documents/${documentId}/blocks`)

export const blockOperationsAPI = (documentId, operations) =>
  // Using http to avoid case conversion.
  http.post(`/documents/${documentId}/blocks/operations`, operations)
