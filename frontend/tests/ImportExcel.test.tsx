import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { ImportExcel } from '../src/pages/ImportExcel'
import { response } from './helpers'

test('import rejects unsupported extension in the UI', async () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<ImportExcel token="token" />)
  await userEvent.upload(screen.getByLabelText(/Choose an Excel workbook/), new File(['text'], 'products.csv'), { applyAccept: false })
  await userEvent.click(screen.getByRole('button', { name: 'Import products' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Select a .xlsx workbook')
  expect(fetchMock).not.toHaveBeenCalled()
})

test('import shows row counts and row errors', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({
    total_rows: 2, valid_rows: 1, invalid_rows: 1, imported: 1,
    errors: [{ row: 3, field: 'quantity', message: 'Quantity must be positive' }],
  })))
  render(<ImportExcel token="token" />)
  await userEvent.upload(screen.getByLabelText(/Choose an Excel workbook/), new File(['xlsx'], 'products.xlsx'))
  expect(screen.getByText('products.xlsx')).toBeInTheDocument()
  await userEvent.click(screen.getByRole('button', { name: 'Import products' }))
  expect(await screen.findByText('Quantity must be positive')).toBeInTheDocument()
  expect(screen.getByText('1 imported')).toBeInTheDocument()
})

test('import shows server error', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(response({ error: { code: 'INVALID_HEADERS', message: 'Invalid headers' } }, 422)))
  render(<ImportExcel token="token" />)
  await userEvent.upload(screen.getByLabelText(/Choose an Excel workbook/), new File(['xlsx'], 'products.xlsx'))
  await userEvent.click(screen.getByRole('button', { name: 'Import products' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Invalid headers')
})
