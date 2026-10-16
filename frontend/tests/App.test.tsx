import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import { App } from '../src/App'
import { response } from './helpers'

test('protected route sends unauthenticated visitor to login', () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<MemoryRouter initialEntries={['/dashboard']}><App /></MemoryRouter>)
  expect(screen.getByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  expect(fetchMock).not.toHaveBeenCalled()
})

test('valid stored session opens dashboard and can sign out', async () => {
  localStorage.setItem('carbontrack_token', 'demo-token')
  vi.stubGlobal('fetch', vi.fn().mockImplementation((url: string) => Promise.resolve(
    url.endsWith('/auth/me')
      ? response({ id: 1, email: 'demo@example.test', role: 'user', is_active: true })
      : response({ total_products: 0, total_quantity: '0', total_direct_emissions: '0',
        total_indirect_emissions: '0', total_emissions: '0', estimated_carbon_cost: '0' }),
  )))
  render(<MemoryRouter initialEntries={['/dashboard']}><App /></MemoryRouter>)
  expect(await screen.findByRole('heading', { name: 'Portfolio dashboard' })).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: 'Sign out' }))
  expect(screen.getByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  expect(localStorage.getItem('carbontrack_token')).toBeNull()
})

test('invalid stored session returns to login', async () => {
  localStorage.setItem('carbontrack_token', 'expired-token')
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({ error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' } }, 401)))
  render(<MemoryRouter initialEntries={['/products']}><App /></MemoryRouter>)
  expect(await screen.findByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
  expect(localStorage.getItem('carbontrack_token')).toBeNull()
})

test('login connects the form to protected navigation', async () => {
  vi.stubGlobal('fetch', vi.fn().mockImplementation((url: string) => Promise.resolve(
    url.endsWith('/auth/login') ? response({ access_token: 'new-token' })
      : url.endsWith('/auth/me') ? response({ id: 1, email: 'demo@example.test', role: 'user', is_active: true })
        : response({ total_products: 0, total_quantity: '0', total_direct_emissions: '0',
          total_indirect_emissions: '0', total_emissions: '0', estimated_carbon_cost: '0' }),
  )))
  render(<MemoryRouter initialEntries={['/login']}><App /></MemoryRouter>)
  await userEvent.type(screen.getByLabelText('Email address'), 'demo@example.test')
  await userEvent.type(screen.getByLabelText('Password'), 'DemoPass123')
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(await screen.findByRole('heading', { name: 'Portfolio dashboard' })).toBeInTheDocument()
  expect(localStorage.getItem('carbontrack_token')).toBe('new-token')
})
