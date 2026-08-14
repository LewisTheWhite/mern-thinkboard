import { useState, useEffect } from 'react'
import { PlusIcon, Trash2Icon, XIcon } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../lib/axios'
import LabelBadge from './LabelBadge'

const ManageLabelsModal = ({ isOpen, onClose }) => {
  const [labels, setLabels] = useState([])
  const [loading, setLoading] = useState(true)
  const [newName, setNewName] = useState('')
  const [newColor, setNewColor] = useState('#10b981')
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    if (!isOpen) return
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
  }, [isOpen])

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!newName.trim()) {
      toast.error('Label name is required')
      return
    }
    if (newName.trim().length > 25) {
      toast.error('Label name must be 25 characters or fewer')
      return
    }
    setCreating(true)
    try {
      const res = await api.post('/labels', { name: newName.trim(), color: newColor })
      setLabels((prev) => [...prev, res.data])
      setNewName('')
      setNewColor('#10b981')
      toast.success('Label created')
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to create label'
      toast.error(message)
    } finally {
      setCreating(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this label? It will be removed from all notes.')) return
    try {
      await api.delete(`/labels/${id}`)
      setLabels((prev) => prev.filter((l) => l._id !== id))
      toast.success('Label deleted')
    } catch (error) {
      const message = error.response?.data?.message || 'Failed to delete label'
      toast.error(message)
    }
  }

  if (!isOpen) return null

  return (
    <div className="modal modal-open">
      <div className="modal-box">
        <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" onClick={onClose}>
          <XIcon className="size-4" />
        </button>
        <h3 className="font-bold text-lg mb-4">Manage Labels</h3>

        {loading ? (
          <p className="text-base-content/60">Loading...</p>
        ) : (
          <div className="space-y-3 mb-6 max-h-60 overflow-y-auto">
            {labels.map((label) => (
              <div key={label._id} className="flex items-center justify-between">
                <LabelBadge label={label} />
                {!label.isDefault && (
                  <button
                    className="btn btn-ghost btn-xs text-error"
                    onClick={() => handleDelete(label._id)}
                  >
                    <Trash2Icon className="size-3.5" />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}

        <form onSubmit={handleCreate} className="flex items-end gap-2">
          <div className="form-control flex-1">
            <label className="label"><span className="label-text">New Label</span></label>
            <input
              type="text"
              className="input input-bordered input-sm"
              placeholder="Label name"
              maxLength={25}
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
            />
          </div>
          <div className="form-control">
            <label className="label"><span className="label-text">Color</span></label>
            <input
              type="color"
              className="w-10 h-8 rounded cursor-pointer border border-base-300"
              value={newColor}
              onChange={(e) => setNewColor(e.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary btn-sm" disabled={creating}>
            <PlusIcon className="size-4" />
          </button>
        </form>
      </div>
      <div className="modal-backdrop" onClick={onClose} />
    </div>
  )
}

export default ManageLabelsModal
