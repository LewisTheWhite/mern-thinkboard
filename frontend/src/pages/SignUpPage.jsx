import { useMemo, useState } from 'react'
import { CheckCircle2Icon, EyeIcon, EyeOffIcon, UserPlusIcon } from 'lucide-react'
import { Link, useNavigate } from 'react-router'
import toast from 'react-hot-toast'
import useAuth from '../hooks/useAuth'

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const SignUpPage = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [errors, setErrors] = useState({})

  const { signup } = useAuth()
  const navigate = useNavigate()

  const validFields = useMemo(
    () => ({
      name: name.trim().length > 0,
      email: EMAIL_REGEX.test(email),
      password: password.length >= 8,
      confirmPassword: confirmPassword.length > 0 && confirmPassword === password,
    }),
    [name, email, password, confirmPassword]
  )

  const validate = () => {
    const nextErrors = {}

    if (!name.trim()) {
      nextErrors.name = 'Name is required'
    }

    if (!email.trim()) {
      nextErrors.email = 'Email is required'
    } else if (!EMAIL_REGEX.test(email)) {
      nextErrors.email = 'Use a valid email format'
    }

    if (!password) {
      nextErrors.password = 'Password is required'
    } else if (password.length < 8) {
      nextErrors.password = 'Password must be at least 8 characters'
    }

    if (!confirmPassword) {
      nextErrors.confirmPassword = 'Please confirm your password'
    } else if (confirmPassword !== password) {
      nextErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!validate()) {
      toast.error('Please complete all required fields correctly')
      return
    }

    setSubmitting(true)
    try {
      await signup({ name, email, password, confirmPassword })
      toast.success('Account created. Please login to continue.')
      navigate('/login')
    } catch (error) {
      const message = error.response?.data?.message || 'Sign up failed. Please try again.'
      toast.error(message)
    } finally {
      setSubmitting(false)
    }
  }

  const inputClass = (field) => `input input-bordered w-full pr-16 ${errors[field] ? 'input-error border-red-300' : ''}`

  const validationIcon = (isValid) => {
    if (!isValid) return null
    return <CheckCircle2Icon className="size-4 text-success absolute right-3 top-1/2 -translate-y-1/2" />
  }

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center px-4 py-8">
      <div className="card w-full max-w-lg bg-base-100 shadow-xl border border-base-content/10">
        <div className="card-body">
          <h1 className="card-title text-2xl mb-2">Create your account</h1>
          <p className="text-base-content/70 mb-4">Join ThinkBoard and start organizing your notes.</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label" htmlFor="signup-name">
                <span className="label-text">Name</span>
              </label>
              <div className="relative">
                <input
                  id="signup-name"
                  type="text"
                  className={inputClass('name')}
                  placeholder="Your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                {validationIcon(validFields.name)}
              </div>
              {errors.name && <p className="text-error text-sm mt-1">{errors.name}</p>}
            </div>

            <div className="form-control">
              <label className="label" htmlFor="signup-email">
                <span className="label-text">Email</span>
              </label>
              <div className="relative">
                <input
                  id="signup-email"
                  type="email"
                  className={inputClass('email')}
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                {validationIcon(validFields.email)}
              </div>
              {errors.email && <p className="text-error text-sm mt-1">{errors.email}</p>}
            </div>

            <div className="form-control">
              <label className="label" htmlFor="signup-password">
                <span className="label-text">Password</span>
              </label>
              <div className="relative">
                <input
                  id="signup-password"
                  type={showPassword ? 'text' : 'password'}
                  className={inputClass('password')}
                  placeholder="Minimum 8 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                {validFields.password && <CheckCircle2Icon className="size-4 text-success absolute right-9 top-1/2 -translate-y-1/2" />}
                <button
                  type="button"
                  className="btn btn-ghost btn-xs absolute right-1 top-1/2 -translate-y-1/2"
                  onClick={() => setShowPassword((prev) => !prev)}
                >
                  {showPassword ? <EyeOffIcon className="size-4" /> : <EyeIcon className="size-4" />}
                </button>
              </div>
              {validFields.password && <p className="text-success text-xs mt-1">Password strength looks good</p>}
              {errors.password && <p className="text-error text-sm mt-1">{errors.password}</p>}
            </div>

            <div className="form-control">
              <label className="label" htmlFor="signup-confirm-password">
                <span className="label-text">Confirm Password</span>
              </label>
              <div className="relative">
                <input
                  id="signup-confirm-password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  className={inputClass('confirmPassword')}
                  placeholder="Re-enter password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {validFields.confirmPassword && <CheckCircle2Icon className="size-4 text-success absolute right-9 top-1/2 -translate-y-1/2" />}
                <button
                  type="button"
                  className="btn btn-ghost btn-xs absolute right-1 top-1/2 -translate-y-1/2"
                  onClick={() => setShowConfirmPassword((prev) => !prev)}
                >
                  {showConfirmPassword ? <EyeOffIcon className="size-4" /> : <EyeIcon className="size-4" />}
                </button>
              </div>
              {validFields.confirmPassword && <p className="text-success text-xs mt-1">Passwords match</p>}
              {errors.confirmPassword && <p className="text-error text-sm mt-1">{errors.confirmPassword}</p>}
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
              <UserPlusIcon className="size-4" />
              {submitting ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <p className="text-sm text-center mt-4">
            Already have an account?{' '}
            <Link to="/login" className="link link-primary">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default SignUpPage
