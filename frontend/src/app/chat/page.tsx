 'use client';

import { useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import { useRouter } from 'next/navigation';
import { useAuthStore, useChatStore, wsMessageToChatMessage } from '@/lib/store';
import { AikoWebSocket } from '@/lib/websocket';
import { TypingIndicator } from '@/components/chat/TypingIndicator';
import { ChatInput } from '@/components/chat/ChatInput';
import { Sidebar } from '@/components/chat/Sidebar';
import { Heart, Loader2 } from 'lucide-react';

// Dynamically load Live2DCanvas to ensure Cubism runtime is loaded first
const Live2DCanvas = dynamic(() => import('@/components/chat/Live2DCanvas').then(mod => ({ default: mod.Live2DCanvas })), {
  ssr: false,
  loading: () => <div className="text-white text-sm">Loading Alexia...</div>,
});

type StagePairPhase = 'entering' | 'visible' | 'exiting';

interface StagePair {
  id: string;
  userContent: string;
  assistantContent: string;
  phase: StagePairPhase;
}

export default function ChatPage() {
  const activeLive2DModel = '/live2d/alexia/Alexia.model3.json';

  const router = useRouter();
  const { isAuthenticated, token, user, initAuth, clearAuth } = useAuthStore();
  const { messages, isTyping, isConnected, addMessage, setTyping, setConnected } = useChatStore();

  const [isLoading, setIsLoading] = useState(true);
  const [stagePairs, setStagePairs] = useState<StagePair[]>([]);
  const wsRef = useRef<AikoWebSocket | null>(null);
  const pendingUserQueueRef = useRef<string[]>([]);
  const activeStageUserRef = useRef<string | null>(null);
  const pairTimersRef = useRef<Map<string, number>>(new Map());

  const showUserStageNow = (userContent: string) => {
    const pairId = `${Date.now()}-${Math.random()}`;
    let exitingIds: string[] = [];
    activeStageUserRef.current = userContent;

    setStagePairs((prev) => {
      exitingIds = prev.map((pair) => pair.id);
      const exiting = prev.map((pair) => ({ ...pair, phase: 'exiting' as const }));
      return [...exiting, { id: pairId, userContent, assistantContent: '', phase: 'entering' as const }];
    });

    const enterTimer = window.setTimeout(() => {
      setStagePairs((prev) =>
        prev.map((pair) => (pair.id === pairId && pair.phase === 'entering' ? { ...pair, phase: 'visible' } : pair))
      );
      pairTimersRef.current.delete(pairId);
    }, 230);
    pairTimersRef.current.set(pairId, enterTimer);

    exitingIds.forEach((oldId) => {
      const existingTimer = pairTimersRef.current.get(oldId);
      if (existingTimer) {
        window.clearTimeout(existingTimer);
      }

      const exitTimer = window.setTimeout(() => {
        setStagePairs((prev) => prev.filter((pair) => pair.id !== oldId));
        pairTimersRef.current.delete(oldId);
      }, 280);

      pairTimersRef.current.set(oldId, exitTimer);
    });
  };

  const attachAssistantToActiveStage = (userContent: string, assistantContent: string) => {
    if (activeStageUserRef.current !== userContent) {
      return;
    }

    setStagePairs((prev) => {
      if (prev.length === 0) {
        return [{
          id: `${Date.now()}-${Math.random()}`,
          userContent,
          assistantContent,
          phase: 'visible',
        }];
      }

      const latest = prev[prev.length - 1];
      return [{ ...latest, assistantContent, phase: 'visible' }];
    });
  };

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  useEffect(() => {
    return () => {
      pairTimersRef.current.forEach((timer) => window.clearTimeout(timer));
      pairTimersRef.current.clear();
    };
  }, []);

  useEffect(() => {
    if (!token) {
      setIsLoading(false);
      return;
    }

    const ws = new AikoWebSocket(token);
    wsRef.current = ws;

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

    ws.on('message', (msg) => {
      if (msg.content) {
        const chatMessage = wsMessageToChatMessage(msg);
        addMessage(chatMessage);

        if (chatMessage.role === 'assistant' && pendingUserQueueRef.current.length > 0) {
          const nextUserMessage = pendingUserQueueRef.current.shift();
          if (nextUserMessage) {
            attachAssistantToActiveStage(nextUserMessage, chatMessage.content);
          }
        }

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

    ws.on('action', (msg) => {
      if (msg.action === 'open_website' && msg.url) {
        window.open(msg.url, '_blank', 'noopener,noreferrer');
      }
    });

    ws.on('error', (msg) => {
      const errorText = (msg.content || '').toLowerCase();
      if (errorText.includes('authentication failed') || errorText.includes('missing authentication')) {
        clearAuth();
        router.push('/login');
        return;
      }

      if (msg.content) {
        addMessage({
          role: 'system',
          content: `Error: ${msg.content}`,
          timestamp: new Date().toISOString(),
        });
      }
      setTyping(false);
    });

    return () => {
      console.log('🔌 Cleaning up WebSocket connection');
      ws.disconnect();
    };
  }, [token, clearAuth, router, addMessage, setTyping, setConnected]);

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

      // Show user bubble immediately without waiting for AI response.
      showUserStageNow(content);
      pendingUserQueueRef.current.push(content);

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
      <div className="flex items-center justify-center min-h-screen bg-[#090b14]">
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
    <div className="relative flex h-screen overflow-hidden bg-[#0a0d17] text-slate-100">
      <div className="ambient-bg" />
      <Sidebar />
      
      {/* Main Chat Area */}
      <main className="relative z-10 flex flex-1 flex-col lg:pl-20">
        {/* Floating AiKO Profile Card */}
        <div className="absolute left-24 top-7 z-30 w-72 rounded-2xl border border-cyan-300/35 bg-slate-900/45 px-4 py-3 backdrop-blur-lg shadow-[0_20px_60px_-20px_rgba(34,211,238,0.3)]">
          <div className="flex items-center gap-3">
            {/* Avatar */}
            <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full border-2 border-fuchsia-400/60 bg-gradient-to-br from-fuchsia-500 to-cyan-500 shadow-[0_0_20px_-8px_rgba(232,121,249,0.8)]">
              <span className="text-base font-semibold text-white">A</span>
            </div>

            {/* Name & Status */}
            <div className="flex-1 min-w-0">
              <p className="truncate text-2xl font-semibold text-slate-100">
                AiKO
              </p>
              <p className="mt-0.5 flex items-center gap-1 text-[12px] text-emerald-300">
                <span className="inline-block h-2 w-2 rounded-full bg-emerald-400" />
                Online
              </p>
            </div>

            {/* Heart Icon */}
            <Heart className="h-6 w-6 flex-shrink-0 cursor-pointer text-slate-400 transition-colors hover:text-fuchsia-300" />
          </div>
        </div>

        {/* Floating Right Controls */}
        <div className="absolute right-4 top-8 z-30 flex items-center space-x-4 lg:right-8">
          <div className="rounded-full border border-cyan-400/25 bg-cyan-500/10 px-4 py-2 backdrop-blur-md shadow-[0_0_30px_-18px_rgba(56,189,248,0.9)]">
            <span className="text-xs font-medium tracking-wide text-cyan-200">Free Version</span>
          </div>

          <div className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border border-fuchsia-300/40 bg-gradient-to-br from-fuchsia-500/80 to-cyan-500/80 font-semibold text-white transition-transform hover:scale-105">
            {user?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
        </div>

        {/* Floating Character Layer */}
        <div className="pointer-events-none absolute left-1/2 top-0 z-10 -translate-x-1/2">
          <div className="relative h-[64vh] w-[280px] sm:w-[340px] lg:w-[400px]">
            <div className="absolute inset-0 rounded-full bg-[radial-gradient(circle_at_center,rgba(236,72,153,0.18)_0%,rgba(34,211,238,0.09)_45%,rgba(10,13,23,0)_75%)] blur-2xl" />
            <Live2DCanvas
              modelPath={activeLive2DModel}
              className="relative z-10 h-full w-full"
            />
          </div>
        </div>

        {/* Floating Stage Chat Stack */}
        <div className="pointer-events-none absolute bottom-32 left-1/2 z-20 w-full max-w-2xl -translate-x-1/2 px-4 ">
          <div className="pointer-events-auto space-y-3">
            {stagePairs.length === 0 ? (
              <div className="mx-auto w-fit rounded-full border border-fuchsia-400/35 bg-fuchsia-500/10 px-6 py-3 text-center">
                <p className="text-lg font-medium text-slate-200">Welcome back, {user?.username || 'friend'}~ what's on your mind?</p>
              </div>
            ) : (
              stagePairs.map((pair) => (
                <div
                  key={pair.id}
                  className={`space-y-2 ${pair.phase === 'entering' ? 'stage-pair-enter' : ''} ${pair.phase === 'exiting' ? 'stage-pair-exit' : ''}`}
                >
                  <div className="flex justify-end">
                    <div className="max-w-[86%] rounded-2xl rounded-br-sm border border-fuchsia-300/40 bg-gradient-to-br from-fuchsia-500/95 to-cyan-500/85 px-4 py-3 shadow-[0_20px_60px_-35px_rgba(6,182,212,0.9)]">
                      <p className="text-sm leading-relaxed text-white">{pair.userContent}</p>
                    </div>
                  </div>

                  <div className="flex justify-start">
                    {pair.assistantContent ? (
                      <div className="glass-panel max-w-[86%] rounded-2xl rounded-bl-sm border border-cyan-200/20 px-4 py-3">
                        <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-100">{pair.assistantContent}</p>
                      </div>
                    ) : (
                      <div className="rounded-full border border-cyan-300/20 bg-slate-900/35 px-3 py-1 text-xs text-cyan-200/80">
                        Aiko is thinking...
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}

            {isTyping && (
              <div className="flex justify-start">
                <TypingIndicator />
              </div>
            )}

            {messages.length > 0 && (
              <div className="flex justify-center pt-1">
                <div className="rounded-full border border-cyan-300/25 bg-slate-900/65 px-5 py-2 text-sm text-cyan-100 backdrop-blur-md">
                  Tap to hear Aiko's voice
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Floating Input Area */}
        <div className="pointer-events-none absolute bottom-6 left-1/2 z-30 w-full max-w-4xl -translate-x-1/2 px-4">
          <div className="pointer-events-auto mx-auto w-full">
            <ChatInput
              onSend={handleSendMessage}
              disabled={!isConnected}
              placeholder={isConnected ? 'Talk with Aiko...' : 'Connecting...'}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
