import { request } from './client'
import type { DashboardSummary } from '../types'

export const dashboardApi = {
  summary: (token: string) => request<DashboardSummary>('/api/v1/dashboard/summary', {}, token),
}
