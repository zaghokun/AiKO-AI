'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { Heart, Loader2 } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, initAuth } = useAuthStore();

  useEffect(() => {
    initAuth();
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/chat');
    } else {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center" style={{ backgroundColor: 'var(--aiko-bg)' }}>
      {/* Brand mark */}
      <div className="mb-6 w-16 h-16 rounded-2xl bg-gradient-to-br from-[var(--aiko-pink)] to-[var(--aiko-purple)] flex items-center justify-center shadow-2xl shadow-[var(--aiko-pink)]/30">
        <Heart className="w-8 h-8 text-white fill-white" />
      </div>

      <h1
        className="text-3xl font-bold mb-2 tracking-tight"
        style={{ color: 'var(--aiko-text)' }}
      >
        AiKO
      </h1>
      <p className="text-sm mb-8" style={{ color: 'var(--aiko-text-muted)' }}>
        Your AI Companion
      </p>

      <div className="flex items-center gap-2" style={{ color: 'var(--aiko-text-muted)' }}>
        <Loader2 className="w-4 h-4 animate-spin" />
        <span className="text-sm">Loading...</span>
      </div>
    </div>
  );
}
