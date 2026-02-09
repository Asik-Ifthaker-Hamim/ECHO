const API_BASE_URL = 'http://localhost:8000'

export const apiClient = {
  async getCommands() {
    const response = await fetch(`${API_BASE_URL}/commands/`)
    if (!response.ok) throw new Error('Failed to fetch commands')
    return response.json()
  },

  async createCommand(commandName, commandPath) {
    const response = await fetch(`${API_BASE_URL}/commands/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command_name: commandName, command_path: commandPath })
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create command')
    }
    return response.json()
  },

  async deleteCommand(commandName) {
    const response = await fetch(`${API_BASE_URL}/commands/${encodeURIComponent(commandName)}`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to delete command')
    }
    return response.json()
  },

  async getSettings() {
    const response = await fetch(`${API_BASE_URL}/settings/`)
    if (!response.ok) throw new Error('Failed to fetch settings')
    return response.json()
  },

  async setSetting(key, value) {
    const response = await fetch(`${API_BASE_URL}/settings/${key}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key, value })
    })
    if (!response.ok) throw new Error('Failed to update setting')
    return response.json()
  },

  async startListening() {
    const response = await fetch(`${API_BASE_URL}/listener/start`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to start listening')
    return response.json()
  },

  async stopListening() {
    const response = await fetch(`${API_BASE_URL}/listener/stop`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to stop listening')
    return response.json()
  }
}
