import api from '@/utils/api'

export async function fetchCurrentPrices(symbols) {
  const res = await api.post('simulation/prices/', { symbols })
  return res.data 
}