'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useAuthStore, useChatStore, wsMessageToChatMessage } from '@/lib/store';
import { AikoWebSocket } from '@/lib/websocket';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { TypingIndicator } from '@/components/chat/TypingIndicator';
import { ChatInput } from '@/components/chat/ChatInput';
import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';
import { Heart, Loader2, Volume2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ChatPage() {
  const router = useRouter();
  const { isAuthenticated, token, initAuth } = useAuthStore();
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
      <div className="flex items-center justify-center min-h-screen" style={{ backgroundColor: 'var(--aiko-bg)' }}>
        <div className="text-center space-y-4">
          <Loader2 className="w-12 h-12 animate-spin mx-auto" style={{ color: 'var(--aiko-pink)' }} />
          <p style={{ color: 'var(--aiko-text-muted)' }}>Connecting to Aiko...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen overflow-hidden" style={{ backgroundColor: 'var(--aiko-bg)' }}>
      <Sidebar />
      <Header title="Chat with Aiko" />

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col lg:ml-20 pt-14 relative">
        {/* Character and Chat Container */}
        <div className="flex-1 flex flex-col items-center justify-center px-4 pt-6 pb-4 overflow-hidden">
          {/* Character Image Placeholder */}
          <div className="relative mb-6 flex-shrink-0">
            <div
              className="w-64 h-80 sm:w-80 sm:h-96 rounded-2xl flex items-center justify-center shadow-2xl"
              style={{
                background: 'linear-gradient(135deg, rgba(233,30,99,0.08), rgba(124,58,237,0.12))',
                border: '2px solid rgba(233,30,99,0.2)',
              }}
            >
              <div className="text-center space-y-3">
                <Heart className="w-16 h-16 mx-auto" style={{ color: 'rgba(233,30,99,0.35)' }} />
                <p className="text-sm font-medium" style={{ color: 'var(--aiko-text-muted)' }}>Character Image</p>
                <p className="text-xs" style={{ color: 'var(--aiko-text-dim)' }}>Coming Soon</p>
              </div>
            </div>
          </div>

          {/* Chat Messages Container */}
          <div className="w-full max-w-3xl flex-1 flex flex-col min-h-0">
            <ScrollArea className="flex-1 px-2">
              <div className="space-y-4 py-4">
                {messages.length === 0 ? (
                  <div className="text-center space-y-4 py-8">
                    <p className="text-sm" style={{ color: 'var(--aiko-text-muted)' }}>Start a conversation with Aiko</p>
                    <p className="text-xs" style={{ color: 'var(--aiko-text-dim)' }}>Type a message below to begin</p>
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
                            <div
                              className="max-w-[85%] rounded-2xl rounded-bl-sm px-4 py-3 shadow-lg"
                              style={{
                                backgroundColor: 'var(--aiko-surface-2)',
                                border: '1px solid var(--aiko-border)',
                                color: 'var(--aiko-text)',
                              }}
                            >
                              <p className="text-sm leading-relaxed whitespace-pre-wrap">
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
                  className="rounded-full px-6 py-2 text-sm"
                  style={{
                    backgroundColor: 'rgba(233,30,99,0.08)',
                    borderColor: 'rgba(233,30,99,0.25)',
                    color: 'var(--aiko-pink-light)',
                  }}
                >
                  <Volume2 className="w-4 h-4 mr-2" />
                  Tap to hear Aiko's voice
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 flex-shrink-0" style={{ borderTop: '1px solid var(--aiko-border)', backgroundColor: 'var(--aiko-surface)' }}>
          <div className="max-w-4xl mx-auto">
            <ChatInput onSend={handleSendMessage} disabled={!isConnected} />
          </div>
        </div>
      </main>
    </div>
  );
}
