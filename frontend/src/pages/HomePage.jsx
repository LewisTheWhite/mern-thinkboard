import { useState, useEffect, useCallback } from "react"
import { FilterIcon } from "lucide-react"
import RateLimitedUI from "../components/RateLimitedUI"
import toast from "react-hot-toast"
import NoteCard from "../components/NoteCard"
import api from "../lib/axios"
import NotesNotFound from "../components/NotesNotFound"
import FilterSidebar from "../components/FilterSidebar"

const HomePage = ({ onNotesCountChange }) => {
  const [isRateLimited, setIsRateLimited] = useState(false)
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({ title: '', labels: [], dateFrom: '', dateTo: '' })

  const fetchNotes = useCallback(async () => {
    try {
      const params = new URLSearchParams()
      if (filters.title) params.set('title', filters.title)
      if (filters.labels && filters.labels.length > 0) params.set('labels', filters.labels.join(','))
      if (filters.dateFrom) params.set('dateFrom', filters.dateFrom)
      if (filters.dateTo) params.set('dateTo', filters.dateTo)

      const queryString = params.toString()
      const res = await api.get(`/notes${queryString ? `?${queryString}` : ''}`)
      setNotes(res.data)
      setIsRateLimited(false)
    } catch (error) {
      console.error("Error fetching notes:", error)
      if (error.response && error.response.status === 429) {
        setIsRateLimited(true)
      } else {
        toast.error("An error occurred while fetching notes. Please try again later.")
      }
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    fetchNotes()
  }, [fetchNotes])

  useEffect(() => {
    onNotesCountChange(notes.length >= 1)
  }, [notes, onNotesCountChange])

  return (
    <div className="min-h-screen">

      {isRateLimited && <RateLimitedUI />}

      <div className="max-w-7xl mx-auto p-4 mt-6">
        {/* Filter toggle button */}
        <div className="flex justify-end mb-4">
          <button
            className={`btn btn-sm ${showFilters ? 'btn-primary' : 'btn-ghost'}`}
            onClick={() => setShowFilters((prev) => !prev)}
          >
            <FilterIcon className="size-4" />
            {showFilters ? 'Hide Filters' : 'Filters'}
          </button>
        </div>

        {loading && <div className="text-center text-primary py-10">Loading notes...</div>}

        {!loading && notes.length === 0 && !isRateLimited && <NotesNotFound />}

        {!loading && notes.length > 0 && !isRateLimited && (
          <div className="flex gap-6">
            <FilterSidebar filters={filters} onFiltersChange={setFilters} isOpen={showFilters} />
            <div className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {notes.map(note => (
                <div key={note._id}>
                  <NoteCard note={note} setNotes={setNotes} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Show sidebar even if no results when filters are active */}
        {!loading && notes.length === 0 && !isRateLimited && showFilters && (
          <div className="flex gap-6">
            <FilterSidebar filters={filters} onFiltersChange={setFilters} isOpen={showFilters} />
            <div className="flex-1 text-center py-10 text-base-content/60">
              No notes match your filters.
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage