'use client';

import { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import {
  MessageCircle,
  User,
  History,
  Settings,
  LogOut,
  Menu,
  X,
  Heart,
} from 'lucide-react';
import { useAuthStore, useChatStore } from '@/lib/store';

interface NavItem {
  icon: React.ElementType;
  label: string;
  href: string;
}

const navItems: NavItem[] = [
  { icon: MessageCircle, label: 'Chat', href: '/chat' },
  { icon: History, label: 'History', href: '/history' },
  { icon: User, label: 'Profile', href: '/profile' },
];

export function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();
  const { user, clearAuth } = useAuthStore();
  const { isConnected } = useChatStore();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const handleLogout = () => {
    clearAuth();
    router.push('/login');
  };

  const handleNav = (href: string) => {
    router.push(href);
    setIsMobileOpen(false);
  };

  return (
    <>
      {/* Mobile toggle button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        aria-label={isMobileOpen ? 'Close menu' : 'Open menu'}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-xl bg-[var(--aiko-surface-2)] border border-[var(--aiko-border)] hover:border-[var(--aiko-pink)]/40 transition-colors"
      >
        {isMobileOpen ? (
          <X className="w-5 h-5 text-[var(--aiko-text-muted)]" />
        ) : (
          <Menu className="w-5 h-5 text-[var(--aiko-text-muted)]" />
        )}
      </button>

      {/* Mobile overlay */}
      {isMobileOpen && (
        <div
          onClick={() => setIsMobileOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
        />
      )}

      {/* Sidebar panel */}
      <aside
        className={[
          'fixed left-0 top-0 h-screen w-20 z-40',
          'flex flex-col py-5 items-center',
          'bg-[var(--aiko-surface)] border-r border-[var(--aiko-border)]',
          'transition-transform duration-300',
          isMobileOpen ? 'translate-x-0' : '-translate-x-full',
          'lg:translate-x-0',
        ].join(' ')}
      >
        {/* Brand icon */}
        <div className="mb-6 flex-shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--aiko-pink)] to-[var(--aiko-purple)] flex items-center justify-center shadow-lg shadow-[var(--aiko-pink)]/30">
            <Heart className="w-5 h-5 text-white fill-white" />
          </div>
        </div>

        {/* User avatar */}
        <div className="mb-5 flex-shrink-0 relative">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[var(--aiko-pink)] to-[var(--aiko-purple)] flex items-center justify-center text-white font-semibold text-lg border-2 border-[var(--aiko-border)] shadow-md">
            {user?.username?.charAt(0).toUpperCase() ?? 'A'}
          </div>
          {/* Online status dot */}
          <span
            className={[
              'absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-[var(--aiko-surface)]',
              isConnected ? 'bg-emerald-500' : 'bg-rose-500',
            ].join(' ')}
          />
        </div>

        {/* Username label */}
        <p className="text-[10px] text-[var(--aiko-text-muted)] font-medium truncate w-16 text-center mb-4 leading-tight">
          {user?.username ?? 'Guest'}
        </p>

        <div className="w-8 h-px bg-[var(--aiko-border)] mb-4" />

        {/* Navigation items */}
        <nav className="flex-1 flex flex-col items-center gap-2 w-full px-3">
          {navItems.map(({ icon: Icon, label, href }) => {
            const isActive = pathname === href;
            return (
              <button
                key={href}
                onClick={() => handleNav(href)}
                title={label}
                className={[
                  'w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200',
                  isActive
                    ? 'bg-[var(--aiko-pink)]/20 text-[var(--aiko-pink-light)] shadow-sm shadow-[var(--aiko-pink)]/20'
                    : 'text-[var(--aiko-text-muted)] hover:bg-[var(--aiko-surface-2)] hover:text-[var(--aiko-pink-light)]',
                ].join(' ')}
              >
                <Icon className="w-5 h-5" />
              </button>
            );
          })}
        </nav>

        <div className="w-8 h-px bg-[var(--aiko-border)] mb-4" />

        {/* Settings & Logout */}
        <div className="flex flex-col items-center gap-2 px-3 flex-shrink-0">
          <button
            onClick={() => handleNav('/settings')}
            title="Settings"
            className={[
              'w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200',
              pathname === '/settings'
                ? 'bg-[var(--aiko-pink)]/20 text-[var(--aiko-pink-light)]'
                : 'text-[var(--aiko-text-muted)] hover:bg-[var(--aiko-surface-2)] hover:text-[var(--aiko-pink-light)]',
            ].join(' ')}
          >
            <Settings className="w-5 h-5" />
          </button>

          <button
            onClick={handleLogout}
            title="Logout"
            className="w-12 h-12 rounded-xl flex items-center justify-center text-[var(--aiko-text-muted)] hover:bg-rose-500/10 hover:text-rose-400 transition-all duration-200"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </aside>
    </>
  );
}
