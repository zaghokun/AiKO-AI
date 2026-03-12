/**
 * AiKO API Client
 * Handles all HTTP requests to the backend API
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('aiko_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('aiko_token');
      localStorage.removeItem('aiko_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  response: string;
  action?: string;
  action_data?: any;
}

export interface SessionInfo {
  session_id: string;
  user_id: string;
  created_at: string;
  expires_at: string;
  message_count: number;
  is_active: boolean;
}

export interface MemoryStats {
  total_memories: number;
  collection_info?: any;
}

// API Functions

// Authentication
export const auth = {
  register: async (username: string, email: string, password: string) => {
    const response = await apiClient.post<User>('/auth/register', {
      username,
      email,
      password,
    });
    return response.data;
  },

  login: async (username: string, password: string) => {
    const response = await apiClient.post<LoginResponse>('/auth/login', {
      username,
      password,
    });
    
    // Store token and fetch user info
    localStorage.setItem('aiko_token', response.data.access_token);
    const user = await auth.getMe();
    localStorage.setItem('aiko_user', JSON.stringify(user));
    
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      localStorage.removeItem('aiko_token');
      localStorage.removeItem('aiko_user');
    }
  },

  getMe: async () => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  getProfile: async () => {
    const response = await apiClient.get('/auth/profile');
    return response.data;
  },
};

// Chat
export const chat = {
  send: async (message: string, history: ChatMessage[] = []) => {
    const response = await apiClient.post<ChatResponse>('/chat', {
      message,
      history,
    });
    return response.data;
  },

  getHistory: async (limit: number = 50) => {
    const response = await apiClient.get('/session/history', {
      params: { limit },
    });
    return response.data;
  },

  getSessionInfo: async () => {
    const response = await apiClient.get<SessionInfo>('/session/info');
    return response.data;
  },
};

// Memory
export const memory = {
  getStats: async () => {
    const response = await apiClient.get<MemoryStats>('/memory/stats');
    return response.data;
  },

  search: async (query: string, limit: number = 5) => {
    const response = await apiClient.post('/memory/search', null, {
      params: { query, limit },
    });
    return response.data;
  },
};

export default apiClient;
