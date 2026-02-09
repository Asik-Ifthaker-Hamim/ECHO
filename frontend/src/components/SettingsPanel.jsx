const SettingsPanel = ({ settings, onVoiceChange }) => {
  return (
    <div className="settings-panel">
      <div className="form-group">
        <label htmlFor="voiceSelect">Voice:</label>
        <select
          id="voiceSelect"
          value={settings.voice || 'male'}
          onChange={(e) => onVoiceChange(e.target.value)}
          className="form-input"
        >
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>
    </div>
  )
}

export default SettingsPanel
