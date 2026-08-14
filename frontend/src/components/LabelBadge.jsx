const LabelBadge = ({ label, onRemove }) => {
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium text-white"
      style={{ backgroundColor: label.color }}
    >
      {label.name}
      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            onRemove(label._id)
          }}
          className="hover:opacity-70 ml-0.5"
        >
          ×
        </button>
      )}
    </span>
  )
}

export default LabelBadge
