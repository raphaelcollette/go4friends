import axios from 'axios'

// BASE axios = No Authorization header attached
const base = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

// AUTH axios = Auto attach Authorization header if token exists
const authAxios = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

authAxios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export { base, authAxios }