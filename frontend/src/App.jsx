import { useState, useEffect } from 'react'
import StatusDisplay from './components/StatusDisplay'
import CommandList from './components/CommandList'
import CommandForm from './components/CommandForm'
import SettingsPanel from './components/SettingsPanel'
import { apiClient } from './services/api'
import './styles/App.css'

function App() {
  const [status, setStatus] = useState({
    message: "Say 'Hey Echo' to activate voice recognition.",
    color: 'blue',
    is_listening: false,
    is_active: false
  })
  const [commands, setCommands] = useState([])
  const [settings, setSettings] = useState({ voice: 'male' })
  const [ws, setWs] = useState(null)

  useEffect(() => {
    loadCommands()
    loadSettings()
    connectWebSocket()

    return () => {
      if (ws) ws.close()
    }
  }, [])

  const connectWebSocket = () => {
    const websocket = new WebSocket('ws://localhost:8000/listener/ws')
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setStatus({
        message: data.message,
        color: data.color,
        is_listening: data.is_listening,
        is_active: data.is_active
      })
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
      setStatus({
        message: 'Backend connection error',
        color: 'red',
        is_listening: false,
        is_active: false
      })
    }

    setWs(websocket)
  }

  const loadCommands = async () => {
    try {
      const data = await apiClient.getCommands()
      setCommands(data)
    } catch (error) {
      console.error('Error loading commands:', error)
    }
  }

  const loadSettings = async () => {
    try {
      const data = await apiClient.getSettings()
      setSettings(data)
    } catch (error) {
      console.error('Error loading settings:', error)
    }
  }

  const handleStartListening = async () => {
    try {
      await apiClient.startListening()
      setStatus(prev => ({ ...prev, is_listening: true }))
    } catch (error) {
      console.error('Error starting listening:', error)
    }
  }

  const handleStopListening = async () => {
    try {
      await apiClient.stopListening()
      setStatus(prev => ({ ...prev, is_listening: false, is_active: false }))
    } catch (error) {
      console.error('Error stopping listening:', error)
    }
  }

  const handleAddCommand = async (commandName, commandPath) => {
    try {
      await apiClient.createCommand(commandName, commandPath)
      loadCommands()
    } catch (error) {
      console.error('Error adding command:', error)
      alert(error.message)
    }
  }

  const handleDeleteCommand = async (commandName) => {
    try {
      await apiClient.deleteCommand(commandName)
      loadCommands()
    } catch (error) {
      console.error('Error deleting command:', error)
      alert(error.message)
    }
  }

  const handleVoiceChange = async (voice) => {
    try {
      await apiClient.setSetting('voice', voice)
      setSettings(prev => ({ ...prev, voice }))
    } catch (error) {
      console.error('Error changing voice:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>ECHO Voice Assistant</h1>
      </header>

      <main className="app-main">
        <StatusDisplay status={status} />

        <div className="control-panel">
          <button 
            onClick={handleStartListening} 
            disabled={status.is_listening}
            className="btn btn-primary"
          >
            Start Listening
          </button>
          <button 
            onClick={handleStopListening} 
            disabled={!status.is_listening}
            className="btn btn-danger"
          >
            Stop Listening
          </button>
        </div>

        <div className="content-grid">
          <div className="panel">
            <h2>Commands</h2>
            <CommandList 
              commands={commands} 
              onDelete={handleDeleteCommand}
            />
          </div>

          <div className="panel">
            <h2>Add New Command</h2>
            <CommandForm onSubmit={handleAddCommand} />
            
            <h2 style={{marginTop: '2rem'}}>Settings</h2>
            <SettingsPanel 
              settings={settings} 
              onVoiceChange={handleVoiceChange}
            />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
