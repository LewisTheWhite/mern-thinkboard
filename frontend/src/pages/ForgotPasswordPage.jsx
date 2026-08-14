import { useState } from 'react'
import { Link } from 'react-router'
import { MailIcon, ArrowLeftIcon } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../lib/axios'

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [errors, setErrors] = useState({})

  const validate = () => {
    const nextErrors = {}

    if (!email.trim()) {
      nextErrors.email = 'Email is required'
    } else if (!EMAIL_REGEX.test(email)) {
      nextErrors.email = 'Use a valid email format'
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
      await api.post('/auth/forgot-password', { email })
      setSubmitted(true)
      toast.success('Check your email for a reset link')
    } catch (error) {
      const message = error.response?.data?.message || 'Something went wrong. Please try again.'
      toast.error(message)
    } finally {
      setSubmitting(false)
    }
  }

  const inputClass = (field) => `input input-bordered w-full ${errors[field] ? 'input-error border-red-300' : ''}`

  if (submitted) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center px-4 py-8">
        <div className="card w-full max-w-md bg-base-100 shadow-xl border border-base-content/10">
          <div className="card-body text-center">
            <div className="bg-primary/10 rounded-full p-4 mx-auto w-fit">
              <MailIcon className="size-8 text-primary" />
            </div>
            <h1 className="card-title text-2xl justify-center mt-4">Check your email</h1>
            <p className="text-base-content/70 mt-2">
              If an account exists for <strong>{email}</strong>, a password reset link has been sent.
            </p>
            <p className="text-base-content/50 text-sm mt-4">
              (For development: check the server console for the reset token)
            </p>
            <Link to="/login" className="btn btn-primary mt-6">
              <ArrowLeftIcon className="size-4" />
              Back to Login
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center px-4 py-8">
      <div className="card w-full max-w-md bg-base-100 shadow-xl border border-base-content/10">
        <div className="card-body">
          <h1 className="card-title text-2xl mb-2">Forgot password?</h1>
          <p className="text-base-content/70 mb-4">
            Enter your email address and we'll send you a link to reset your password.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label" htmlFor="forgot-email">
                <span className="label-text">Email</span>
              </label>
              <input
                id="forgot-email"
                type="email"
                placeholder="name@example.com"
                className={inputClass('email')}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {errors.email && <p className="text-error text-sm mt-1">{errors.email}</p>}
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={submitting}>
              <MailIcon className="size-4" />
              {submitting ? 'Sending...' : 'Send Reset Link'}
            </button>
          </form>

          <p className="text-sm text-center mt-4">
            Remember your password?{' '}
            <Link to="/login" className="link link-primary">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default ForgotPasswordPage
