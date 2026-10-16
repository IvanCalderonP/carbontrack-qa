import { FormEvent, useState } from 'react'
import { authApi } from '../api/auth'

export function Login({ onLogin }: { onLogin: (token: string) => void }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!email.includes('@') || !password) {
      setError('Enter a valid email and password.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const result = await authApi.login(email, password)
      onLogin(result.access_token)
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Sign in failed')
    } finally {
      setLoading(false)
    }
  }

  return <div className="login-shell">
    <div className="login-story">
      <div className="brand"><span className="brand-mark">C</span><span>CarbonTrack <small>QA</small></span></div>
      <div><p className="eyebrow">PORTFOLIO PROJECT</p><h1>Make every carbon data point count.</h1>
        <p className="story-copy">A compact, test driven workspace for fictional product portfolios, emissions calculations, and Excel ingestion.</p></div>
      <p className="story-foot">Simplified educational calculations · Independent project</p>
    </div>
    <div className="login-panel">
      <form className="login-card" onSubmit={submit} noValidate>
        <p className="eyebrow">WELCOME BACK</p><h2>Sign in</h2>
        <p className="muted">Explore the QA automation demo workspace.</p>
        <label htmlFor="email">Email address</label>
        <input id="email" type="email" autoComplete="email" value={email} onChange={event => setEmail(event.target.value)} />
        <label htmlFor="password">Password</label>
        <input id="password" type="password" autoComplete="current-password" value={password} onChange={event => setPassword(event.target.value)} />
        {error && <p role="alert" className="error-box">{error}</p>}
        <button className="primary full" type="submit" disabled={loading}>{loading ? 'Signing in…' : 'Sign in'}</button>
        <p className="login-hint">Run the optional seed command for a demo account.</p>
      </form>
    </div>
  </div>
}
