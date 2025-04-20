import axios from 'axios'
import router from '@/router'

// BASE axios = No Authorization header
const base = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

// AUTH axios = Attach token + Handle token expiration
const authAxios = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

// Attach token before every request
authAxios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Intercept failed responses (401 errors) to refresh token automatically
authAxios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        // Call refresh endpoint to get a new access token
        const res = await base.post('users/token/refresh/', {
          refresh: refreshToken,
        })

        const newAccessToken = res.data.access
        localStorage.setItem('access_token', newAccessToken)

        // Retry the original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
        return authAxios(originalRequest)
      } catch (refreshError) {
        // Refresh failed ➔ Logout user
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export { base, authAxios }
