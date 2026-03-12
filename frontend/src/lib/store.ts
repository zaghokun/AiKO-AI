/**
 * Global State Management with Zustand
 */

import { create } from 'zustand';
import { User } from './api';
import { WebSocketMessage } from './websocket';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  memories_used?: number;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  initAuth: () => void;
}

interface ChatState {
  messages: Message[];
  isTyping: boolean;
  isConnected: boolean;
  addMessage: (message: Omit<Message, 'id'>) => void;
  setTyping: (isTyping: boolean) => void;
  setConnected: (isConnected: boolean) => void;
  clearMessages: () => void;
  loadHistory: (messages: Message[]) => void;
}

// Auth Store
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: (user, token) => {
    localStorage.setItem('aiko_token', token);
    localStorage.setItem('aiko_user', JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },

  clearAuth: () => {
    localStorage.removeItem('aiko_token');
    localStorage.removeItem('aiko_user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  initAuth: () => {
    const token = localStorage.getItem('aiko_token');
    const userStr = localStorage.getItem('aiko_user');
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        set({ user, token, isAuthenticated: true });
      } catch (error) {
        console.error('Failed to parse user from localStorage:', error);
        localStorage.removeItem('aiko_token');
        localStorage.removeItem('aiko_user');
      }
    }
  },
}));

// Chat Store
export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isTyping: false,
  isConnected: false,

  addMessage: (message) => {
    const newMessage: Message = {
      ...message,
      id: `${Date.now()}-${Math.random()}`,
    };
    
    set((state) => ({
      messages: [...state.messages, newMessage],
    }));
  },

  setTyping: (isTyping) => set({ isTyping }),

  setConnected: (isConnected) => set({ isConnected }),

  clearMessages: () => set({ messages: [] }),

  loadHistory: (messages) => set({ messages }),
}));

// Helper to convert WebSocket message to Chat message
export function wsMessageToChatMessage(wsMsg: WebSocketMessage): Omit<Message, 'id'> {
  return {
    role: wsMsg.role || 'system',
    content: wsMsg.content || '',
    timestamp: wsMsg.timestamp || new Date().toISOString(),
    memories_used: wsMsg.memories_used,
  };
}
