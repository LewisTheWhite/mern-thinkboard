import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router'
import { EyeIcon, EyeOffIcon, KeyIcon } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../lib/axios'

const ResetPasswordPage = () => {
  const { token } = useParams()
  const navigate = useNavigate()

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const nextErrors = {}

    if (!password) {
      nextErrors.password = 'Password is required'
    } else if (password.length < 8) {
      nextErrors.password = 'Password must be at least 8 characters'
    }

    if (!confirmPassword) {
      nextErrors.confirmPassword = 'Please confirm your password'
    } else if (password !== confirmPassword) {
      nextErrors.confirmPassword = 'Passwords do not match'
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
      await api.post('/auth/reset-password', { token, password, confirmPassword })
      toast.success('Password reset successful! Please sign in.')
      navigate('/login')
    } catch (error) {
      const message = error.response?.data?.message || 'Reset failed. The link may have expired.'
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
          <h1 className="card-title text-2xl mb-2">Reset your password</h1>
          <p className="text-base-content/70 mb-4">
            Enter your new password below.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label" htmlFor="reset-password">
                <span className="label-text">New Password</span>
              </label>
              <div className="relative">
                <input
                  id="reset-password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="At least 8 characters"
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

            <div className="form-control">
              <label className="label" htmlFor="reset-confirm">
                <span className="label-text">Confirm Password</span>
              </label>
              <div className="relative">
                <input
                  id="reset-confirm"
                  type={showConfirm ? 'text' : 'password'}
                  placeholder="Repeat your password"
                  className={`${inputClass('confirmPassword')} pr-10`}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="btn btn-ghost btn-xs absolute right-1 top-1/2 -translate-y-1/2"
                  onClick={() => setShowConfirm((prev) => !prev)}
                >
                  {showConfirm ? <EyeOffIcon className="size-4" /> : <EyeIcon className="size-4" />}
                </button>
              </div>
              {errors.confirmPassword && <p className="text-error text-sm mt-1">{errors.confirmPassword}</p>}
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
              <KeyIcon className="size-4" />
              {submitting ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>

          <p className="text-sm text-center mt-4">
            <Link to="/login" className="link link-primary">
              Back to Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default ResetPasswordPage
