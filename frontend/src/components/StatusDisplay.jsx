const StatusDisplay = ({ status }) => {
  const getStatusColor = () => {
    switch (status.color) {
      case 'green': return '#4CAF50'
      case 'red': return '#f44336'
      case 'blue': return '#2196F3'
      default: return '#ffffff'
    }
  }

  return (
    <div className="status-display">
      <div 
        className={`status-indicator ${status.is_active ? 'active' : ''}`}
        style={{ backgroundColor: getStatusColor() }}
      ></div>
      <p className="status-message" style={{ color: getStatusColor() }}>
        {status.message}
      </p>
      <div className="status-badges">
        {status.is_listening && (
          <span className="badge badge-success">Listening</span>
        )}
        {status.is_active && (
          <span className="badge badge-warning">Active</span>
        )}
      </div>
    </div>
  )
}

export default StatusDisplay
