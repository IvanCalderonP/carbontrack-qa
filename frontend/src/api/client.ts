import type { ApiErrorBody } from '../types'

const baseUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message)
  }
}

export async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const headers = new Headers(options.headers)
  if (token) headers.set('Authorization', `Bearer ${token}`)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  let response: Response
  try {
    response = await fetch(`${baseUrl}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR', 'Cannot reach the API. Check that the backend is running.')
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({})) as ApiErrorBody
    throw new ApiError(response.status, body.error?.code ?? 'HTTP_ERROR', body.error?.message ?? 'Request failed')
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
