import { useEffect, useState } from 'react'
import { dashboardApi } from '../api/dashboard'
import type { DashboardSummary } from '../types'
import { formatNumber } from '../utils/format'

export function Dashboard({ token }: { token: string }) {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    dashboardApi.summary(token).then(result => { if (active) setData(result) })
      .catch(reason => { if (active) setError(reason instanceof Error ? reason.message : 'Unable to load summary') })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [token])

  return <>
    <div className="page-head"><div><p className="eyebrow">OVERVIEW</p><h1>Portfolio dashboard</h1>
      <p className="muted">A quick view of your fictional product emissions.</p></div><span className="pill">Educational demo</span></div>
    {loading && <p role="status" className="panel">Loading dashboard…</p>}
    {error && <p role="alert" className="error-box">{error}</p>}
    {data && <>
      {data.total_products === 0 && <p className="empty-banner">No products yet. Import a workbook or add a product to see your summary.</p>}
      <div className="metric-grid">
        {[
          ['Total products', data.total_products, '01'],
          ['Total emissions', `${formatNumber(data.total_emissions)} tCO₂e`, '02'],
          ['Direct emissions', `${formatNumber(data.total_direct_emissions)} tCO₂e`, '03'],
          ['Indirect emissions', `${formatNumber(data.total_indirect_emissions)} tCO₂e`, '04'],
          ['Estimated carbon cost', `€${formatNumber(data.estimated_carbon_cost)}`, '05'],
        ].map(([label, value, index]) => <article className="metric-card" key={label}>
          <div className="metric-top"><span>{label}</span><span>{index}</span></div>
          <strong>{value}</strong><span className="metric-foot">Portfolio total</span>
        </article>)}
      </div>
      <div className="panel insight"><div><p className="eyebrow">HOW IT WORKS</p><h2>Clear calculations, testable outcomes.</h2>
        <p>Totals combine direct and indirect emissions. Estimated cost multiplies each product’s total emissions by its fictional carbon price.</p></div>
        <div className="formula">total = direct + indirect<br />cost = total × price</div></div>
    </>}
  </>
}
