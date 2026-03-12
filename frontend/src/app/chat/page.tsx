'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useAuthStore, useChatStore, wsMessageToChatMessage } from '@/lib/store';
import { AikoWebSocket } from '@/lib/websocket';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { TypingIndicator } from '@/components/chat/TypingIndicator';
import { ChatInput } from '@/components/chat/ChatInput';
import { Sidebar } from '@/components/chat/Sidebar';
import { Heart, Loader2, Volume2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ChatPage() {
  const router = useRouter();
  const { isAuthenticated, token, user, initAuth } = useAuthStore();
  const { messages, isTyping, isConnected, addMessage, setTyping, setConnected } = useChatStore();
  
  const [isLoading, setIsLoading] = useState(true);
  const wsRef = useRef<AikoWebSocket | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Initialize auth
  useEffect(() => {
    initAuth();
  }, [initAuth]);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Initialize WebSocket
  useEffect(() => {
    if (!token) {
      setIsLoading(false);
      return;
    }

    const ws = new AikoWebSocket(token);
    wsRef.current = ws;

    // Connect
    ws.connect()
      .then(() => {
        console.log('✅ Connected to AiKO');
        setConnected(true);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('❌ Failed to connect:', error);
        setConnected(false);
        setIsLoading(false);
      });

    // Handle messages
    ws.on('message', (msg) => {
      if (msg.content) {
        addMessage(wsMessageToChatMessage(msg));
        setTyping(false);
      }
    });

    ws.on('typing', (msg) => {
      setTyping(msg.is_typing ?? false);
    });

    ws.on('system', (msg) => {
      if (msg.content) {
        addMessage(wsMessageToChatMessage(msg));
      }
    });

    ws.on('error', (msg) => {
      if (msg.content) {
        addMessage({
          role: 'system',
          content: `Error: ${msg.content}`,
          timestamp: new Date().toISOString(),
        });
      }
      setTyping(false);
    });

    // Cleanup
    return () => {
      console.log('🔌 Cleaning up WebSocket connection');
      ws.disconnect();
    };
  }, [token]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isTyping]);

  const handleSendMessage = async (content: string) => {
    if (!wsRef.current?.isConnected()) {
      addMessage({
        role: 'system',
        content: 'Not connected to server. Please refresh the page.',
        timestamp: new Date().toISOString(),
      });
      return;
    }

    try {
      // Add user message to UI
      addMessage({
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      });

      // Send via WebSocket
      wsRef.current.sendMessage(content);
    } catch (error) {
      console.error('Failed to send message:', error);
      addMessage({
        role: 'system',
        content: 'Failed to send message. Please try again.',
        timestamp: new Date().toISOString(),
      });
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-950 via-purple-950/20 to-gray-950">
        <div className="text-center space-y-4">
          <Loader2 className="w-12 h-12 animate-spin text-purple-500 mx-auto" />
          <p className="text-gray-400">Connecting to Aiko...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-950 via-purple-950/20 to-gray-950 overflow-hidden">
      <Sidebar />
      
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col lg:ml-20 relative">
        {/* Top Bar */}
        <div className="absolute top-0 right-0 left-0 z-10 flex items-center justify-between p-4 bg-gradient-to-b from-gray-950/80 to-transparent backdrop-blur-sm">
          <div className="lg:hidden w-16" /> {/* Spacer for mobile menu */}
          
          <div className="flex-1" />
          
          {/* Trial Badge */}
          <div className="flex items-center space-x-4">
            <div className="px-4 py-2 rounded-full bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-500/30">
              <span className="text-xs font-medium text-amber-400">Free Version</span>
            </div>
            
            {/* User Avatar */}
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-semibold cursor-pointer hover:scale-105 transition-transform">
              {user?.username?.charAt(0).toUpperCase() || 'U'}
            </div>
          </div>
        </div>

        {/* Character and Chat Container */}
        <div className="flex-1 flex flex-col items-center justify-center px-4 pt-20 pb-4 overflow-hidden">
          {/* Character Image Placeholder */}
          <div className="relative mb-6 flex-shrink-0">
            <div className="w-64 h-80 sm:w-80 sm:h-96 rounded-2xl bg-gradient-to-br from-purple-900/30 via-pink-900/20 to-purple-900/30 border-2 border-purple-500/30 flex items-center justify-center backdrop-blur-sm shadow-2xl">
              <div className="text-center space-y-3">
                <Heart className="w-16 h-16 text-purple-400/50 mx-auto" />
                <p className="text-gray-400 text-sm font-medium">Character Image</p>
                <p className="text-gray-600 text-xs">Coming Soon</p>
              </div>
            </div>
          </div>

          {/* Chat Messages Container */}
          <div className="w-full max-w-3xl flex-1 flex flex-col min-h-0">
            <ScrollArea className="flex-1 px-2">
              <div className="space-y-4 py-4">
                {messages.length === 0 ? (
                  <div className="text-center space-y-4 py-8">
                    <p className="text-gray-500 text-sm">Start a conversation with Aiko</p>
                    <p className="text-gray-600 text-xs">Type a message below to begin</p>
                  </div>
                ) : (
                  <>
                    {messages.map((message, index) => {
                      if (message.role === 'user') {
                        return (
                          <div key={index} className="flex justify-end">
                            <div className="max-w-[85%] bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl rounded-br-sm px-4 py-3 shadow-lg">
                              <p className="text-white text-sm leading-relaxed">{message.content}</p>
                            </div>
                          </div>
                        );
                      } else if (message.role === 'assistant') {
                        return (
                          <div key={index} className="flex justify-start">
                            <div className="max-w-[85%] bg-gray-800/80 backdrop-blur-sm border border-gray-700/50 rounded-2xl rounded-bl-sm px-4 py-3 shadow-lg">
                              <p className="text-gray-100 text-sm leading-relaxed whitespace-pre-wrap">
                                {message.content}
                              </p>
                            </div>
                          </div>
                        );
                      } else {
                        return (
                          <div key={index} className="flex justify-center">
                            <div className="px-3 py-1.5 rounded-full bg-yellow-500/10 border border-yellow-500/20">
                              <p className="text-xs text-yellow-400">{message.content}</p>
                            </div>
                          </div>
                        );
                      }
                    })}
                    {isTyping && (
                      <div className="flex justify-start">
                        <TypingIndicator />
                      </div>
                    )}
                  </>
                )}
                <div ref={scrollRef} />
              </div>
            </ScrollArea>

            {/* Voice Button (if has messages) */}
            {messages.length > 0 && (
              <div className="flex justify-center py-3 flex-shrink-0">
                <Button
                  variant="outline"
                  className="rounded-full px-6 py-2 bg-purple-900/20 border-purple-500/30 hover:bg-purple-900/40 text-purple-300 text-sm"
                >
                  <Volume2 className="w-4 h-4 mr-2" />
                  Tap to hear Aiko's voice
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-800/50 bg-gray-900/50 backdrop-blur-sm p-4 flex-shrink-0">
          <div className="max-w-4xl mx-auto">
            <ChatInput onSend={handleSendMessage} disabled={!isConnected} />
          </div>
        </div>
      </main>
    </div>
  );
}
