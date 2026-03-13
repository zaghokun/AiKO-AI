/**
 * WebSocket Client for Real-time Chat
 * Handles WebSocket connection to AiKO backend
 */

export type MessageType = 'message' | 'typing' | 'system' | 'error' | 'stream_chunk' | 'pong' | 'action';

export interface WebSocketMessage {
  type: MessageType;
  content?: string;
  role?: 'user' | 'assistant' | 'system';
  timestamp?: string;
  is_typing?: boolean;
  memories_used?: number;
  action?: 'open_website';
  website?: string;
  url?: string;
}

export type WebSocketEventHandler = (message: WebSocketMessage) => void;

export class AikoWebSocket {
  private ws: WebSocket | null = null;
  private token: string;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;
  private eventHandlers: Map<string, WebSocketEventHandler[]> = new Map();
  private intentionalClose = false; // Flag to prevent auto-reconnect on intentional close

  constructor(token: string) {
    this.token = token;
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = process.env.NEXT_PUBLIC_WS_URL || 'localhost:8000';
    this.url = `${wsProtocol}//${wsHost}/ws/chat?token=${token}`;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.intentionalClose = false; // Reset flag when connecting
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('✅ WebSocket Connected');
          this.reconnectAttempts = 0;
          this.startPingInterval();
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data: WebSocketMessage = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onerror = (error) => {
          console.error('❌ WebSocket Error:', error);
          this.emit('error', { type: 'error', content: 'Connection error' });
        };

        this.ws.onclose = (event) => {
          console.log('🔌 WebSocket Closed:', event.code, event.reason);
          this.stopPingInterval();

          // Only auto-reconnect if not intentionally closed
          if (!this.intentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            console.log(`⏱️ Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts})`);
            
            this.reconnectTimeout = setTimeout(() => {
              this.connect();
            }, delay);
          } else if (!this.intentionalClose) {
            this.emit('error', { 
              type: 'error', 
              content: 'Failed to reconnect. Please refresh the page.' 
            });
          }
        };

        // Timeout if connection takes too long
        setTimeout(() => {
          if (this.ws?.readyState !== WebSocket.OPEN) {
            reject(new Error('Connection timeout'));
            this.ws?.close();
          }
        }, 10000);

      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect() {
    this.intentionalClose = true; // Set flag to prevent auto-reconnect
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    this.stopPingInterval();
    this.ws?.close();
    this.ws = null;
  }

  sendMessage(content: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'message',
        content,
      }));
    } else {
      throw new Error('WebSocket is not connected');
    }
  }

  sendStream(content: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'stream',
        content,
      }));
    } else {
      throw new Error('WebSocket is not connected');
    }
  }

  private startPingInterval() {
    this.pingInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000); // Ping every 30 seconds
  }

  private stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private handleMessage(message: WebSocketMessage) {
    const handlers = this.eventHandlers.get(message.type) || [];
    handlers.forEach(handler => handler(message));

    // Also emit to 'all' handlers
    const allHandlers = this.eventHandlers.get('all') || [];
    allHandlers.forEach(handler => handler(message));
  }

  on(event: MessageType | 'all', handler: WebSocketEventHandler) {
    const handlers = this.eventHandlers.get(event) || [];
    handlers.push(handler);
    this.eventHandlers.set(event, handlers);
  }

  off(event: MessageType | 'all', handler: WebSocketEventHandler) {
    const handlers = this.eventHandlers.get(event) || [];
    const index = handlers.indexOf(handler);
    if (index > -1) {
      handlers.splice(index, 1);
      this.eventHandlers.set(event, handlers);
    }
  }

  private emit(event: string, message: WebSocketMessage) {
    const handlers = this.eventHandlers.get(event) || [];
    handlers.forEach(handler => handler(message));
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  getReadyState(): number | null {
    return this.ws?.readyState ?? null;
  }
}

export default AikoWebSocket;
