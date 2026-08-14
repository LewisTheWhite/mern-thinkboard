import HomePage from './pages/HomePage'
import CreatePage from './pages/CreatePage'
import NoteDetailPage from './pages/NoteDetailPage'
import LoginPage from './pages/LoginPage'
import SignUpPage from './pages/SignUpPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import NavBar from './components/NavBar'
import ProtectedRoute from './components/ProtectedRoute'

import { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router'

const THEMES = ['light', 'dark', 'forest', 'synthwave', 'retro', 'cyberpunk', 'valentine', 'halloween', 'garden', 'winter']

const App = () => {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme')
    return savedTheme && THEMES.includes(savedTheme) ? savedTheme : 'garden'
  })
  const [hasNotes, setHasNotes] = useState(false)

  useEffect(() => {
    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <div data-theme={theme} className="min-h-screen">
      <div className='absolute inset-0 -z-10 h-full w-full items-center px-5 py-24 [background:radial-gradient(125%_125%_at_50%_50%,_10%, primary_100%)]' />
      <NavBar theme={theme} setTheme={setTheme} themes={THEMES} hasNotes={hasNotes} />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage onNotesCountChange={setHasNotes} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create"
          element={
            <ProtectedRoute>
              <CreatePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/note/:id"
          element={
            <ProtectedRoute>
              <NoteDetailPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  )
}

export default App