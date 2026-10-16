import { useEffect, useState } from 'react'
import { Navigate, NavLink, Route, Routes, useNavigate } from 'react-router-dom'
import { authApi } from './api/auth'
import { Dashboard } from './pages/Dashboard'
import { ImportExcel } from './pages/ImportExcel'
import { Login } from './pages/Login'
import { Products } from './pages/Products'

export function App() {
  const [token, setToken] = useState(() => localStorage.getItem('carbontrack_token') ?? '')
  const [checking, setChecking] = useState(Boolean(token))
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) return
    let active = true
    authApi.me(token).catch(() => {
      if (active) {
        localStorage.removeItem('carbontrack_token')
        setToken('')
        setChecking(false)
      }
    }).finally(() => { if (active) setChecking(false) })
    return () => { active = false }
  }, [token])

  function login(accessToken: string) {
    localStorage.setItem('carbontrack_token', accessToken)
    setToken(accessToken)
    setChecking(false)
    navigate('/dashboard')
  }

  function logout() {
    localStorage.removeItem('carbontrack_token')
    setToken('')
    navigate('/login')
  }

  if (checking) return <div className="centered"><p role="status">Checking your session…</p></div>
  if (!token) return <Routes>
    <Route path="/login" element={<Login onLogin={login} />} />
    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes>

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">C</span><span>CarbonTrack <small>QA</small></span></div>
      <p className="sidebar-label">WORKSPACE</p>
      <nav aria-label="Main navigation">
        <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>▦ <span>Dashboard</span></NavLink>
        <NavLink to="/products" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>◈ <span>Products</span></NavLink>
        <NavLink to="/import" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>⇧ <span>Import Excel</span></NavLink>
      </nav>
      <div className="sidebar-foot">
        <p>Educational demo<br /><span>Not official CBAM reporting</span></p>
        <button className="logout" onClick={logout}>Sign out</button>
      </div>
    </aside>
    <div className="main-area">
      <header className="topbar"><span>Carbon accounting / QA portfolio</span><span className="status-dot">Demo environment</span></header>
      <main>
        <Routes>
          <Route path="/dashboard" element={<Dashboard token={token} />} />
          <Route path="/products" element={<Products token={token} />} />
          <Route path="/import" element={<ImportExcel token={token} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  </div>
}
