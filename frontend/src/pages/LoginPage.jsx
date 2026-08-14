import { useState } from 'react'
import { EyeIcon, EyeOffIcon, LogInIcon } from 'lucide-react'
import { Link, useNavigate } from 'react-router'
import toast from 'react-hot-toast'
import useAuth from '../hooks/useAuth'

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [errors, setErrors] = useState({})

  const { login } = useAuth()
  const navigate = useNavigate()

  const validate = () => {
    const nextErrors = {}

    if (!email.trim()) {
      nextErrors.email = 'Email is required'
    } else if (!EMAIL_REGEX.test(email)) {
      nextErrors.email = 'Use a valid email format'
    }

    if (!password) {
      nextErrors.password = 'Password is required'
    }

    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!validate()) {
      toast.error('Please fix the highlighted fields')
      return
    }

    setSubmitting(true)
    try {
      await login({ email, password })
      toast.success('Login successful')
      navigate('/')
    } catch (error) {
      const message = error.response?.data?.message || 'Login failed. Please try again.'
      toast.error(message)
    } finally {
      setSubmitting(false)
    }
  }

  const inputClass = (field) => `input input-bordered w-full ${errors[field] ? 'input-error border-red-300' : ''}`

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center px-4 py-8">
      <div className="card w-full max-w-md bg-base-100 shadow-xl border border-base-content/10">
        <div className="card-body">
          <h1 className="card-title text-2xl mb-2">Welcome back</h1>
          <p className="text-base-content/70 mb-4">Sign in to continue managing your notes.</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label" htmlFor="login-email">
                <span className="label-text">Email</span>
              </label>
              <input
                id="login-email"
                type="email"
                placeholder="name@example.com"
                className={inputClass('email')}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {errors.email && <p className="text-error text-sm mt-1">{errors.email}</p>}
            </div>

            <div className="form-control">
              <label className="label" htmlFor="login-password">
                <span className="label-text">Password</span>
              </label>
              <div className="relative">
                <input
                  id="login-password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Your password"
                  className={`${inputClass('password')} pr-10`}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="btn btn-ghost btn-xs absolute right-1 top-1/2 -translate-y-1/2"
                  onClick={() => setShowPassword((prev) => !prev)}
                >
                  {showPassword ? <EyeOffIcon className="size-4" /> : <EyeIcon className="size-4" />}
                </button>
              </div>
              {errors.password && <p className="text-error text-sm mt-1">{errors.password}</p>}
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
              <LogInIcon className="size-4" />
              {submitting ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-sm text-center mt-2">
            <Link to="/forgot-password" className="link link-primary">
              Forgot password?
            </Link>
          </p>

          <p className="text-sm text-center mt-2">
            New here?{' '}
            <Link to="/signup" className="link link-primary">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
