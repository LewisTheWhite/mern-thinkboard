import { LoaderIcon } from 'lucide-react'
import { Navigate } from 'react-router'
import useAuth from '../hooks/useAuth'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, authLoading } = useAuth()

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoaderIcon className="size-10 animate-spin text-primary" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
