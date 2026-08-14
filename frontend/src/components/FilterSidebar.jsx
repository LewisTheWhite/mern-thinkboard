import { useEffect, useState, useRef } from 'react'
import { FilterXIcon, SearchIcon } from 'lucide-react'
import api from '../lib/axios'

const FilterSidebar = ({ filters, onFiltersChange, isOpen }) => {
  const [labels, setLabels] = useState([])
  const [titleInput, setTitleInput] = useState(filters.title || '')
  const debounceRef = useRef(null)

  useEffect(() => {
    const fetchLabels = async () => {
      try {
        const res = await api.get('/labels')
        setLabels(res.data)
      } catch (error) {
        console.error('Error fetching labels for filter:', error)
      }
    }
    fetchLabels()
  }, [])

  // Debounce title search
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      onFiltersChange({ ...filters, title: titleInput })
    }, 300)
    return () => clearTimeout(debounceRef.current)
  }, [titleInput])

  const handleLabelToggle = (labelId) => {
    const current = filters.labels || []
    const updated = current.includes(labelId)
      ? current.filter((id) => id !== labelId)
      : [...current, labelId]
    onFiltersChange({ ...filters, labels: updated })
  }

  const handleDateChange = (field, value) => {
    onFiltersChange({ ...filters, [field]: value })
  }

  const clearFilters = () => {
    setTitleInput('')
    onFiltersChange({ title: '', labels: [], dateFrom: '', dateTo: '' })
  }

  const hasActiveFilters = filters.title || (filters.labels && filters.labels.length > 0) || filters.dateFrom || filters.dateTo

  if (!isOpen) return null

  return (
    <aside className="w-64 shrink-0 bg-base-100 border-r border-base-content/10 p-4 space-y-5 h-fit sticky top-4 rounded-lg shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-sm">Filters</h3>
        {hasActiveFilters && (
          <button className="btn btn-ghost btn-xs text-error" onClick={clearFilters}>
            <FilterXIcon className="size-3.5" />
            Clear
          </button>
        )}
      </div>

      {/* Title Search */}
      <div className="form-control">
        <label className="label py-1">
          <span className="label-text text-xs font-medium">Search by Title</span>
        </label>
        <div className="relative">
          <SearchIcon className="size-4 absolute left-3 top-1/2 -translate-y-1/2 text-base-content/40" />
          <input
            type="text"
            className="input input-bordered input-sm w-full pl-9"
            placeholder="Search notes..."
            value={titleInput}
            onChange={(e) => setTitleInput(e.target.value)}
          />
        </div>
      </div>

      {/* Labels */}
      <div className="form-control">
        <label className="label py-1">
          <span className="label-text text-xs font-medium">Labels</span>
        </label>
        <div className="space-y-1.5 max-h-40 overflow-y-auto">
          {labels.map((label) => (
            <label key={label._id} className="flex items-center gap-2 cursor-pointer hover:bg-base-200 rounded px-1 py-0.5">
              <input
                type="checkbox"
                className="checkbox checkbox-xs"
                checked={(filters.labels || []).includes(label._id)}
                onChange={() => handleLabelToggle(label._id)}
              />
              <span
                className="w-2.5 h-2.5 rounded-full shrink-0"
                style={{ backgroundColor: label.color }}
              />
              <span className="text-xs">{label.name}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Date Range */}
      <div className="form-control">
        <label className="label py-1">
          <span className="label-text text-xs font-medium">Date Range</span>
        </label>
        <div className="space-y-2">
          <input
            type="date"
            className="input input-bordered input-sm w-full"
            value={filters.dateFrom || ''}
            onChange={(e) => handleDateChange('dateFrom', e.target.value)}
          />
          <input
            type="date"
            className="input input-bordered input-sm w-full"
            value={filters.dateTo || ''}
            onChange={(e) => handleDateChange('dateTo', e.target.value)}
          />
        </div>
      </div>
    </aside>
  )
}

export default FilterSidebar
