import { FormEvent, useEffect, useState } from 'react'
import { productsApi } from '../api/products'
import type { ProductInput, ProductPage } from '../types'
import { formatNumber } from '../utils/format'

const emptyProduct: ProductInput = {
  name: '', cn_code: '', country_of_origin: '', quantity: '', unit: 'tonnes',
  direct_emissions: '', indirect_emissions: '', carbon_price: '',
}

export function Products({ token }: { token: string }) {
  const [data, setData] = useState<ProductPage | null>(null)
  const [search, setSearch] = useState('')
  const [country, setCountry] = useState('')
  const [page, setPage] = useState(1)
  const [revision, setRevision] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState<ProductInput>(emptyProduct)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  useEffect(() => {
    let active = true
    const params = new URLSearchParams({ page: String(page), page_size: '8', sort_by: 'created_at', sort_order: 'desc' })
    if (search) params.set('search', search)
    if (country) params.set('country_of_origin', country.toUpperCase())
    productsApi.list(token, params).then(result => {
      if (active) { setData(result); setError('') }
    }).catch(reason => {
      if (active) setError(reason instanceof Error ? reason.message : 'Unable to load products')
    }).finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [token, page, search, country, revision])

  function change(field: keyof ProductInput, value: string) {
    setForm(current => ({ ...current, [field]: value }))
  }

  async function create(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      await productsApi.create(token, { ...form, country_of_origin: form.country_of_origin.toUpperCase() })
      setForm(emptyProduct)
      setShowForm(false)
      setPage(1)
      setRevision(value => value + 1)
    } catch (reason) {
      setFormError(reason instanceof Error ? reason.message : 'Could not create product')
    } finally {
      setSaving(false)
    }
  }

  async function remove(id: number) {
    try {
      await productsApi.remove(token, id)
      setRevision(value => value + 1)
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Could not delete product')
    }
  }

  return <>
    <div className="page-head"><div><p className="eyebrow">PORTFOLIO</p><h1>Products</h1>
      <p className="muted">Explore, filter, and manage fictional product records.</p></div>
      <button className="primary" onClick={() => setShowForm(value => !value)}>{showForm ? 'Close form' : '+ Add product'}</button></div>
    {showForm && <form className="panel product-form" onSubmit={create}>
      <div className="section-title"><h2>New product</h2><span className="muted">All values are fictional.</span></div>
      <div className="form-grid">
        {([
          ['name', 'Product name', 'text'], ['cn_code', 'CN code', 'text'],
          ['country_of_origin', 'Country (ISO 2)', 'text'], ['quantity', 'Quantity', 'number'],
          ['unit', 'Unit', 'text'], ['direct_emissions', 'Direct emissions', 'number'],
          ['indirect_emissions', 'Indirect emissions', 'number'], ['carbon_price', 'Carbon price', 'number'],
        ] as const).map(([field, label, type]) => <label key={field}>{label}
          <input required type={type} min={field === 'quantity' ? '0.0000000001' : undefined} step={type === 'number' ? 'any' : undefined}
            value={form[field]} onChange={event => change(field, event.target.value)} />
        </label>)}
      </div>
      {formError && <p role="alert" className="error-box">{formError}</p>}
      <button className="primary" disabled={saving}>{saving ? 'Saving…' : 'Save product'}</button>
    </form>}
    <section className="panel">
      <div className="section-title"><div><h2>Product portfolio</h2><p className="muted">{data?.total ?? 0} products in this view</p></div>
        <div className="filters"><label className="sr-only" htmlFor="search">Search products</label>
          <input id="search" placeholder="Search products" value={search} onChange={event => { setSearch(event.target.value); setPage(1) }} />
          <label className="sr-only" htmlFor="country">Country code</label>
          <input id="country" placeholder="Country code" maxLength={2} value={country} onChange={event => { setCountry(event.target.value); setPage(1) }} />
        </div></div>
      {loading && <p role="status">Loading products…</p>}
      {error && <p role="alert" className="error-box">{error}</p>}
      {!loading && !error && data?.items.length === 0 && <p className="empty-banner">No products match this view.</p>}
      {!loading && !error && data && data.items.length > 0 && <>
        <div className="table-wrap"><table><thead><tr><th>Product</th><th>CN code</th><th>Country</th><th>Quantity</th><th>Unit</th><th>Direct</th><th>Indirect</th><th>Total</th><th>Price</th><th>Actions</th></tr></thead>
          <tbody>{data.items.map(product => <tr key={product.id}><td className="product-name">{product.name}</td><td>{product.cn_code}</td><td><span className="country-tag">{product.country_of_origin}</span></td>
            <td>{formatNumber(product.quantity)}</td><td>{product.unit}</td><td>{formatNumber(product.direct_emissions)}</td><td>{formatNumber(product.indirect_emissions)}</td><td><strong>{formatNumber(product.total_emissions)}</strong></td><td>€{formatNumber(product.carbon_price)}</td>
            <td><button className="text-button" onClick={() => remove(product.id)} aria-label={`Delete ${product.name}`}>Delete</button></td></tr>)}</tbody></table></div>
        <div className="pagination"><span>Page {data.page} of {data.pages}</span><div>
          <button onClick={() => setPage(value => value - 1)} disabled={page <= 1}>Previous</button>
          <button onClick={() => setPage(value => value + 1)} disabled={page >= data.pages}>Next</button>
        </div></div>
      </>}
    </section>
  </>
}
