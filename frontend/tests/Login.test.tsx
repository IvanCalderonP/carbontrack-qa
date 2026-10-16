import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { Login } from '../src/pages/Login'
import { response } from './helpers'

test('login validates input before requesting API', async () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<Login onLogin={vi.fn()} />)
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Enter a valid email')
  expect(fetchMock).not.toHaveBeenCalled()
})

test('login shows API error for wrong credentials', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({ error: { code: 'INVALID_CREDENTIALS', message: 'Invalid email or password' } }, 401)))
  render(<Login onLogin={vi.fn()} />)
  await userEvent.type(screen.getByLabelText('Email address'), 'student@example.test')
  await userEvent.type(screen.getByLabelText('Password'), 'wrong')
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password')
})

test('login submits credentials and returns token', async () => {
  const fetchMock = vi.fn().mockResolvedValue(response({ access_token: 'test-token' }))
  const onLogin = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<Login onLogin={onLogin} />)
  await userEvent.type(screen.getByLabelText('Email address'), 'student@example.test')
  await userEvent.type(screen.getByLabelText('Password'), 'Password123')
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(onLogin).toHaveBeenCalledWith('test-token')
  expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/auth/login'), expect.objectContaining({ method: 'POST' }))
})

test('login shows network failure', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')))
  render(<Login onLogin={vi.fn()} />)
  await userEvent.type(screen.getByLabelText('Email address'), 'student@example.test')
  await userEvent.type(screen.getByLabelText('Password'), 'Password123')
  await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Cannot reach the API')
})
