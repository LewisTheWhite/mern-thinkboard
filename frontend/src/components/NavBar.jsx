import { Link, useLocation } from "react-router"
import { LogInIcon, LogOutIcon, PlusIcon, TagIcon, UserPlusIcon } from "lucide-react"
import { useState } from "react"
import useAuth from "../hooks/useAuth"
import ManageLabelsModal from "./ManageLabelsModal"


const NavBar = ({ theme = 'garden', setTheme = () => {}, themes = [], hasNotes = false }) => {
  const { pathname } = useLocation()
  const { isAuthenticated, user, logout } = useAuth()
  const [showLabelsModal, setShowLabelsModal] = useState(false)

  const isAuthRoute = pathname === '/login' || pathname === '/signup'

  return (
    <>
    <header className="bg-base-300 border-b border-base-content/10">
        <div className="mx-auto max-w-6xl p-4">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-primary font-mono tracking-tigher">ThinkBoard</h1>
                <div className="flex items-center gap-4">
                    {pathname === "/" && isAuthenticated && hasNotes && (
                      <Link to={"/create"} className="btn btn-primary">
                          <PlusIcon className="size-5"/>
                          <span>New Note</span>
                      </Link>
                    )}
                    {isAuthenticated && (
                      <button className="btn btn-ghost btn-sm" onClick={() => setShowLabelsModal(true)}>
                        <TagIcon className="size-4" />
                        Labels
                      </button>
                    )}
                    {!isAuthenticated && !isAuthRoute && (
                      <>
                        <Link to="/login" className="btn btn-ghost btn-sm">
                          <LogInIcon className="size-4" />
                          Login
                        </Link>
                        <Link to="/signup" className="btn btn-primary btn-sm">
                          <UserPlusIcon className="size-4" />
                          Sign Up
                        </Link>
                      </>
                    )}
                </div>
                <div className="flex items-center gap-3">
                  {isAuthenticated && <span className="text-sm text-base-content/70 hidden md:inline">Hello, {user?.name}</span>}
                  <label htmlFor="theme-select" className="text-sm font-medium">
                    Theme
                  </label>
                  <select
                    id="theme-select"
                    className="select select-bordered select-sm"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                  >
                    {themes.map((themeName) => (
                      <option key={themeName} value={themeName}>
                        {themeName.charAt(0).toUpperCase() + themeName.slice(1)}
                      </option>
                    ))}
                  </select>
                    {isAuthenticated && (
                      <button type="button" className="btn btn-outline btn-sm" onClick={logout}>
                        <LogOutIcon className="size-4" />
                        Logout
                      </button>
                    )}
                </div>
            </div>
        </div>
    </header>
    <ManageLabelsModal isOpen={showLabelsModal} onClose={() => setShowLabelsModal(false)} />
    </>
  )
}

export default NavBar