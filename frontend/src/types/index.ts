export interface User {
  id: number
  email: string
  role: 'user' | 'admin'
  is_active: boolean
  created_at: string
}

export interface ProductInput {
  name: string
  cn_code: string
  country_of_origin: string
  quantity: string
  unit: string
  direct_emissions: string
  indirect_emissions: string
  carbon_price: string
}

export interface Product extends ProductInput {
  id: number
  owner_id: number
  total_emissions: string
  emission_intensity: string
  estimated_carbon_cost: string
  created_at: string
  updated_at: string
}

export interface ProductPage {
  items: Product[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface DashboardSummary {
  total_products: number
  total_quantity: string
  total_direct_emissions: string
  total_indirect_emissions: string
  total_emissions: string
  estimated_carbon_cost: string
}

export interface ImportResult {
  total_rows: number
  valid_rows: number
  invalid_rows: number
  imported: number
  errors: { row: number; field: string; message: string }[]
}

export interface ApiErrorBody {
  error?: { code: string; message: string; issues?: { field: string; message: string }[] }
}
