import axios from 'axios'

const api = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const token = localStorage.getItem('token')
        const response = await axios.post('/', {
          url: '/api/auth/refresh',
          headers: { Authorization: `Bearer ${token}` }
        })
        
        const newToken = response.data.access_token
        localStorage.setItem('token', newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
