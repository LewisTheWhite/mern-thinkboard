import { useState, useEffect } from "react"
import { useNavigate, useParams } from "react-router"
import { LoaderIcon, Trash2Icon, ArrowLeftIcon } from "lucide-react"
import { Link } from "react-router"

import api from "../lib/axios"
import toast from "react-hot-toast"
import LabelSelector from "../components/LabelSelector"
import LabelBadge from "../components/LabelBadge"

const NoteDetailPage = () => {
  const [note, setNote] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const navigate = useNavigate()

  const {id} = useParams() // Get the note ID from the URL parameters
  console.log("Note ID from params:", id)

  useEffect(() => {
    const fetchNote = async () => {
      try {
        const res = await api.get(`/notes/${id}`)
        setNote(res.data)
      } catch (error) {
        toast.error("Failed to fetch note details. Please try again later.")
        console.error("Error fetching note details:", error)
      } finally {
        setLoading(false)

      }
    }
    fetchNote()
  }, [id])

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this note?")) return
    try {
      await api.delete(`/notes/${id}`)
      toast.success("Note deleted successfully")
      navigate("/")
    } catch (error) {
      toast.error("Failed to delete note. Please try again later.")
      console.error("Error deleting note:", error)
    }
  }
  const handleSave = async () => {
    if(!note.title.trim() || !note.content.trim()) {
      toast.error("Title and content cannot be empty.")
      return
    }

    setSaving(true)

    try {

      const payload = {
        title: note.title,
        content: note.content,
        labels: note.labels?.map((l) => (typeof l === 'object' ? l._id : l)) || [],
      }
      await api.put(`/notes/${id}`, payload)
      toast.success("Note updated successfully")
      navigate("/")

    } catch (error) {

      toast.error("Failed to update note. Please try again later.")
      console.error("Error updating note:", error)

    } finally {

      setSaving(false)

    }
  }


  if (loading) {
    return (
      <div className="min-h-screen bg-base-200 flex items-center justify-center">
        <LoaderIcon className="size-10 animate-spin" />
      </div>
    )
  }


  return (
    <div className="min-h-screen bg-base-200">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <Link to="/" className="btn btn-ghost">
              <ArrowLeftIcon className="h-5 w-5" />
              Back to Notes
            </Link>
            <button onClick={handleDelete} className="btn btn-error btn-outline">
              <Trash2Icon className="h-5 w-5" />
              Delete Note
            </button>
          </div>
          <div className="card bg-base-100">
            <div className="card-body">
              <div className="form-control mb-4">
                <label className="label">
                  <span className="label-text">Title</span>
                </label>
                <input type="text" className="input input-bordered" placeholder="Note title" value={note?.title} onChange={(e) => setNote({ ...note, title: e.target.value })} />
              </div>
              <div className="form-control">
                <label className="label">
                  <span className="label-text">Content</span>
                </label>
                <textarea className="textarea textarea-bordered h-40" placeholder="Note content" value={note.content} onChange={(e) => setNote({ ...note, content: e.target.value })} />
              </div>
              <div className="form-control mt-4">
                <label className="label">
                  <span className="label-text">Labels</span>
                </label>
                <LabelSelector
                  selectedIds={note.labels?.map((l) => (typeof l === 'object' ? l._id : l)) || []}
                  onChange={(ids) => setNote({ ...note, labels: ids })}
                />
              </div>
              <div className="card-actions justify-end">
                <button className="btn btn-primary" disabled={saving} onClick={handleSave}>
                  {saving ?  "Saving..." : "Save Changes"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>  
    </div>
  )
}

export default NoteDetailPage