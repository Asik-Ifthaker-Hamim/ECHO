const CommandList = ({ commands, onDelete }) => {
  return (
    <div className="command-list">
      {commands.length === 0 ? (
        <p className="empty-state">No commands available</p>
      ) : (
        <div className="command-grid">
          {commands.map((cmd) => (
            <div key={cmd.id} className="command-item">
              <div className="command-info">
                <strong>{cmd.command_name}</strong>
                <small className="command-path">{cmd.command_path}</small>
                {cmd.is_preset && <span className="badge badge-info">Preset</span>}
              </div>
              {!cmd.is_preset && (
                <button 
                  onClick={() => onDelete(cmd.command_name)}
                  className="btn btn-sm btn-danger"
                >
                  Delete
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default CommandList
