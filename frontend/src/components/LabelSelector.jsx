import { useEffect, useState } from 'react'
import api from '../lib/axios'
import LabelBadge from './LabelBadge'

const LabelSelector = ({ selectedIds = [], onChange }) => {
  const [labels, setLabels] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLabels = async () => {
      try {
        const res = await api.get('/labels')
        setLabels(res.data)
      } catch (error) {
        console.error('Error fetching labels:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchLabels()
  }, [])

  const toggle = (id) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((l) => l !== id))
    } else {
      onChange([...selectedIds, id])
    }
  }

  if (loading) {
    return <span className="text-sm text-base-content/50">Loading labels...</span>
  }

  return (
    <div className="flex flex-wrap gap-2">
      {labels.map((label) => {
        const isSelected = selectedIds.includes(label._id)
        return (
          <button
            key={label._id}
            type="button"
            onClick={() => toggle(label._id)}
            className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium border-2 transition-all ${
              isSelected ? 'text-white border-transparent' : 'text-base-content border-base-300 opacity-60 hover:opacity-100'
            }`}
            style={isSelected ? { backgroundColor: label.color, borderColor: label.color } : {}}
          >
            <span
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: label.color }}
            />
            {label.name}
          </button>
        )
      })}
    </div>
  )
}

export default LabelSelector
