import { render, screen } from '@testing-library/react'
import { vi } from 'vitest'
import { Dashboard } from '../src/pages/Dashboard'
import { response } from './helpers'

const summary = {
  total_products: 2, total_quantity: '15', total_direct_emissions: '3',
  total_indirect_emissions: '2', total_emissions: '5', estimated_carbon_cost: '200',
}

test('dashboard shows loading and five metrics', async () => {
  let complete: (value: Response) => void = () => undefined
  vi.stubGlobal('fetch', vi.fn().mockReturnValue(new Promise<Response>(resolve => { complete = resolve })))
  render(<Dashboard token="token" />)
  expect(screen.getByRole('status')).toHaveTextContent('Loading dashboard')
  complete(response(summary))
  expect(await screen.findByText('€200')).toBeInTheDocument()
  expect(screen.getByText('Total products')).toBeInTheDocument()
  expect(screen.getByText('Direct emissions')).toBeInTheDocument()
})

test('dashboard explains empty portfolio', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({ ...summary, total_products: 0 })))
  render(<Dashboard token="token" />)
  expect(await screen.findByText(/No products yet/)).toBeInTheDocument()
})

test('dashboard shows API error', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({ error: { code: 'ERROR', message: 'Server unavailable' } }, 500)))
  render(<Dashboard token="token" />)
  expect(await screen.findByRole('alert')).toHaveTextContent('Server unavailable')
})
