import { request } from './client'
import type { User } from '../types'

export const authApi = {
  login: (email: string, password: string) => request<{ access_token: string }>(
    '/api/v1/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) },
  ),
  me: (token: string) => request<User>('/api/v1/auth/me', {}, token),
}
