import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { Products } from '../src/pages/Products'
import { product, response } from './helpers'

test('products renders rows and searches by name', async () => {
  const fetchMock = vi.fn().mockResolvedValue(response({ items: [product], total: 1, page: 1, page_size: 8, pages: 1 }))
  vi.stubGlobal('fetch', fetchMock)
  render(<Products token="token" />)
  expect(await screen.findByText('Sample steel')).toBeInTheDocument()
  await userEvent.type(screen.getByLabelText('Search products'), 'steel')
  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('search=steel'), expect.anything()))
})

test('products shows empty state and API error', async () => {
  const fetchMock = vi.fn().mockResolvedValue(response({ error: { code: 'ERROR', message: 'Database unavailable' } }, 500))
    .mockResolvedValueOnce(response({ items: [], total: 0, page: 1, page_size: 8, pages: 0 }))
  vi.stubGlobal('fetch', fetchMock)
  render(<Products token="token" />)
  expect(await screen.findByText('No products match this view.')).toBeInTheDocument()
  await userEvent.type(screen.getByLabelText('Country code'), 'TR')
  expect(await screen.findByRole('alert')).toHaveTextContent('Database unavailable')
})

test('products paginates to next page', async () => {
  const fetchMock = vi.fn().mockImplementation((url: string) => Promise.resolve(response({
    items: [product], total: 9, page: url.includes('page=2') ? 2 : 1, page_size: 8, pages: 2,
  })))
  vi.stubGlobal('fetch', fetchMock)
  render(<Products token="token" />)
  await screen.findByText('Page 1 of 2')
  await userEvent.click(screen.getByRole('button', { name: 'Next' }))
  expect(await screen.findByText('Page 2 of 2')).toBeInTheDocument()
})

test('products creates a product with entered values', async () => {
  const fetchMock = vi.fn().mockImplementation((_url: string, options: RequestInit) => Promise.resolve(
    options.method === 'POST' ? response(product, 201) : response({ items: [product], total: 1, page: 1, page_size: 8, pages: 1 }),
  ))
  vi.stubGlobal('fetch', fetchMock)
  render(<Products token="token" />)
  await screen.findByText('Sample steel')
  await userEvent.click(screen.getByRole('button', { name: /Add product/ }))
  for (const [label, value] of [
    ['Product name', 'Sample steel'], ['CN code', '720810'], ['Country (ISO 2)', 'TR'],
    ['Quantity', '10'], ['Direct emissions', '2'], ['Indirect emissions', '1'], ['Carbon price', '40'],
  ]) await userEvent.type(screen.getByLabelText(label), value)
  await userEvent.click(screen.getByRole('button', { name: 'Save product' }))
  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/api/v1/products'), expect.objectContaining({ method: 'POST' })))
  expect(screen.queryByText('New product')).not.toBeInTheDocument()
})

test('products can delete a row', async () => {
  const fetchMock = vi.fn().mockImplementation((_url: string, options: RequestInit) => Promise.resolve(
    options.method === 'DELETE' ? { ok: true, status: 204 } : response({ items: [product], total: 1, page: 1, page_size: 8, pages: 1 }),
  ))
  vi.stubGlobal('fetch', fetchMock)
  render(<Products token="token" />)
  await screen.findByText('Sample steel')
  await userEvent.click(screen.getByRole('button', { name: 'Delete Sample steel' }))
  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/products/1'), expect.objectContaining({ method: 'DELETE' })))
})
