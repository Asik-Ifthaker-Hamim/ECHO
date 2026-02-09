import { useState } from 'react'

const CommandForm = ({ onSubmit }) => {
  const [commandName, setCommandName] = useState('')
  const [commandPath, setCommandPath] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (commandName.trim() && commandPath.trim()) {
      onSubmit(commandName.trim(), commandPath.trim())
      setCommandName('')
      setCommandPath('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="command-form">
      <div className="form-group">
        <label htmlFor="commandName">Command Name:</label>
        <input
          type="text"
          id="commandName"
          value={commandName}
          onChange={(e) => setCommandName(e.target.value)}
          placeholder="e.g., open notepad"
          className="form-input"
        />
      </div>
      <div className="form-group">
        <label htmlFor="commandPath">Application Path:</label>
        <input
          type="text"
          id="commandPath"
          value={commandPath}
          onChange={(e) => setCommandPath(e.target.value)}
          placeholder="e.g., C:\\Windows\\System32\\notepad.exe"
          className="form-input"
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Add Command
      </button>
    </form>
  )
}

export default CommandForm
