import type { Log } from '@/types/WebSocketServiceTypes'
import type { IWebSocketService } from '@/interfaces/IWebSocketService'

class WebSocketService implements IWebSocketService {
  private socket: WebSocket | null = null
  private eventListeners: ((log: Log) => void)[] = []

  public connect(port: string) {
    this.socket = new WebSocket(`${port}`)

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.notifyListeners(data)
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    this.socket.onerror = (error) => {
      console.error('WebSocket Error:', error)
    }

    this.socket.onclose = () => {
      console.log('WebSocket connection closed')
    }
  }

  public subscribe(listener: (log: Log) => void) {
    this.eventListeners.push(listener)
  }

  public unsubscribe(listener: (log: Log) => void) {
    this.eventListeners = this.eventListeners.filter((l) => l !== listener)
  }

  public notifyListeners(log: Log) {
    this.eventListeners.forEach((listener) => listener(log))
  }

  public disconnect() {
    if (this.socket) {
      console.log('this.socket:', this.socket)
      this.socket.close()
      console.log('WebSocket disconnected')
    } else {
      console.log('WebSocket already disconnected')
    }
  }
}

export const webSocketService = new WebSocketService()
