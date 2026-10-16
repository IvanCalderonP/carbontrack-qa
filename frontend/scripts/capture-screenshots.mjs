import { chromium } from 'playwright-core'
import { resolve } from 'node:path'

const apiUrl = process.env.VITE_API_URL ?? 'http://localhost:8000'
const uiUrl = process.env.UI_URL ?? 'http://localhost:5173'
const email = process.env.DEMO_EMAIL ?? 'demo@example.test'
const password = process.env.DEMO_PASSWORD ?? 'DemoPass123'
const imageDir = resolve('../docs/images')

const login = await fetch(`${apiUrl}/api/v1/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
})
if (!login.ok) throw new Error('Demo login failed. Run the backend seed command first.')
const { access_token: token } = await login.json()

const browser = await chromium.launch({ channel: 'msedge', headless: true })
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 1 })
  await page.addInitScript(value => localStorage.setItem('carbontrack_token', value), token)

  await page.goto(`${uiUrl}/dashboard`)
  await page.getByText('Estimated carbon cost').waitFor()
  await page.screenshot({ path: resolve(imageDir, 'dashboard.png'), fullPage: true })

  await page.goto(`${uiUrl}/products`)
  await page.getByText('Sample steel coil').waitFor()
  await page.screenshot({ path: resolve(imageDir, 'products.png'), fullPage: true })

  await page.goto(`${uiUrl}/import`)
  await page.locator('#workbook').setInputFiles(resolve('../sample-data/invalid_products.xlsx'))
  await page.getByRole('button', { name: 'Import products' }).click()
  await page.getByRole('region', { name: 'Import result' }).waitFor()
  await page.screenshot({ path: resolve(imageDir, 'import.png'), fullPage: true })

  console.log('Captured dashboard.png, products.png, and import.png from the running UI.')
} finally {
  await browser.close()
}
