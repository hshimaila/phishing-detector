import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
})

export const scanEmail = (text) =>
  api.post('/scan/email', { text }).then(r => r.data)

export const scanUrl = (url) =>
  api.post('/scan/url', { url }).then(r => r.data)

export const getHistory = (params = {}) =>
  api.get('/history', { params }).then(r => r.data)

export const deleteScan = (id) =>
  api.delete(`/history/${id}`).then(r => r.data)

export const getHealth = () =>
  api.get('/health').then(r => r.data)

export default api