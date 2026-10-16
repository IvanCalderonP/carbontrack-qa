import { FormEvent, useState } from 'react'
import { importsApi } from '../api/imports'
import type { ImportResult } from '../types'

export function ImportExcel({ token }: { token: string }) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<ImportResult | null>(null)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!file || !file.name.toLowerCase().endsWith('.xlsx')) {
      setError('Select a .xlsx workbook.')
      return
    }
    setLoading(true)
    setError('')
    setResult(null)
    try {
      setResult(await importsApi.products(token, file))
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Import failed')
    } finally {
      setLoading(false)
    }
  }

  return <>
    <div className="page-head"><div><p className="eyebrow">DATA INGESTION</p><h1>Import products</h1>
      <p className="muted">Validate a fictional product workbook before it enters your portfolio.</p></div></div>
    <div className="import-grid"><section className="panel">
      <h2>Upload workbook</h2><p className="muted">Only .xlsx files, up to 2 MiB and 1,000 rows.</p>
      <form onSubmit={submit}>
        <label className="dropzone" htmlFor="workbook"><span className="upload-icon">⇧</span><strong>Choose an Excel workbook</strong>
          <span>{file?.name ?? 'No file selected'}</span></label>
        <input id="workbook" type="file" accept=".xlsx" onChange={event => setFile(event.target.files?.[0] ?? null)} />
        {error && <p role="alert" className="error-box">{error}</p>}
        <button className="primary" disabled={loading}>{loading ? 'Uploading…' : 'Import products'}</button>
      </form>
    </section><aside className="panel guidance"><p className="eyebrow">REQUIRED COLUMNS</p>
      <ol><li>product_name</li><li>cn_code</li><li>country_of_origin</li><li>quantity</li><li>unit</li><li>direct_emissions</li><li>indirect_emissions</li><li>carbon_price</li></ol>
      <p className="muted">Use the sample files in <code>sample-data/</code> to explore valid and invalid rows.</p>
    </aside></div>
    {result && <section className="panel import-result" aria-label="Import result">
      <div className="section-title"><h2>Import result</h2><span className="pill">{result.imported} imported</span></div>
      <div className="result-stats"><span>Total rows <strong>{result.total_rows}</strong></span><span>Valid rows <strong>{result.valid_rows}</strong></span><span>Invalid rows <strong>{result.invalid_rows}</strong></span></div>
      {result.errors.length > 0 && <div className="table-wrap"><table><thead><tr><th>Row</th><th>Field</th><th>Message</th></tr></thead>
        <tbody>{result.errors.map((item, index) => <tr key={`${item.row}-${item.field}-${index}`}><td>{item.row}</td><td>{item.field}</td><td>{item.message}</td></tr>)}</tbody></table></div>}
      {result.errors.length === 0 && <p className="success-text">All rows passed validation.</p>}
    </section>}
  </>
}
