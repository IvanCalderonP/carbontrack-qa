export function response(body: unknown, status = 200): Response {
  return { ok: status >= 200 && status < 300, status, json: async () => body } as Response
}

export const product = {
  id: 1, owner_id: 1, name: 'Sample steel', cn_code: '720810', country_of_origin: 'TR',
  quantity: '10', unit: 'tonnes', direct_emissions: '2', indirect_emissions: '1',
  total_emissions: '3', carbon_price: '40', estimated_carbon_cost: '120', emission_intensity: '0.3',
  created_at: '2026-01-01T00:00:00Z', updated_at: '2026-01-01T00:00:00Z',
}
