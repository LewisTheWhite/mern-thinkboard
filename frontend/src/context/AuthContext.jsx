import { createContext, useEffect, useMemo, useState } from 'react'
import toast from 'react-hot-toast'
import api from '../lib/axios'

export const AuthContext = createContext(null)

const TOKEN_KEY = 'authToken'
const USER_KEY = 'authUser'

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [user, setUser] = useState(() => {
    const rawUser = localStorage.getItem(USER_KEY)
    return rawUser ? JSON.parse(rawUser) : null
  })
  const [authLoading, setAuthLoading] = useState(true)

  useEffect(() => {
    const bootstrap = async () => {
      const storedToken = localStorage.getItem(TOKEN_KEY)
      if (!storedToken) {
        setAuthLoading(false)
        return
      }

      try {
        const res = await api.get('/auth/me')
        setUser(res.data)
      } catch (error) {
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(USER_KEY)
        setToken('')
        setUser(null)
      } finally {
        setAuthLoading(false)
      }
    }

    bootstrap()
  }, [])

  const signup = async (payload) => {
    const response = await api.post('/auth/signup', payload)
    return response.data
  }

  const login = async ({ email, password }) => {
    const response = await api.post('/auth/login', { email, password })
    const data = response.data

    setToken(data.token)
    setUser(data.user)
    localStorage.setItem(TOKEN_KEY, data.token)
    localStorage.setItem(USER_KEY, JSON.stringify(data.user))

    return data
  }

  const logout = () => {
    setToken('')
    setUser(null)
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    toast.success('Logged out successfully')
  }

  const value = useMemo(
    () => ({
      token,
      user,
      authLoading,
      isAuthenticated: Boolean(token),
      signup,
      login,
      logout,
    }),
    [token, user, authLoading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
