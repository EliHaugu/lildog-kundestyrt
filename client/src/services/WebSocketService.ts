import type { Log } from '@/types/WebSocketServiceTypes'
import type { IWebSocketService } from '@/interfaces/IWebSocketService'

class WebSocketService implements IWebSocketService {
  private socket: WebSocket | null = null
  private eventListeners: ((log: Log) => void)[] = []

  public connect(port: number) {
    this.socket = new WebSocket(`ws://localhost:${port}/ws/logs/`)  

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        
        if (Array.isArray(data)) {
          data.forEach((log: Log) => {
            if (log.id && log.name && Array.isArray(log.log)) {
              this.notifyListeners(log) 
              console.log('WebSocket message received:', log)
            } else {
              console.error('Invalid log format:', log)
            }
          })
        } else {
          console.error('Expected an array but received:', data)
        }
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
}

export const webSocketService = new WebSocketService()
