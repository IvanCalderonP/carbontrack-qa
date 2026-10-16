import { request } from './client'
import type { ImportResult } from '../types'

export const importsApi = {
  products: (token: string, file: File) => {
    const body = new FormData()
    body.append('file', file)
    return request<ImportResult>('/api/v1/imports/products', { method: 'POST', body }, token)
  },
}
