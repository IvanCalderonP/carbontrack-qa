import { request } from './client'
import type { Product, ProductInput, ProductPage } from '../types'

export const productsApi = {
  list: (token: string, params: URLSearchParams) => request<ProductPage>(`/api/v1/products?${params}`, {}, token),
  create: (token: string, product: ProductInput) => request<Product>(
    '/api/v1/products', { method: 'POST', body: JSON.stringify(product) }, token,
  ),
  remove: (token: string, id: number) => request<void>(`/api/v1/products/${id}`, { method: 'DELETE' }, token),
}
