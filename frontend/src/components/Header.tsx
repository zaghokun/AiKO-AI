'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ChevronDown, User, Settings, LogOut, Sparkles } from 'lucide-react';
import { useAuthStore } from '@/lib/store';

interface HeaderProps {
  /** Optional page title shown in the center/left of the header */
  title?: string;
}

export function Header({ title }: HeaderProps) {
  const router = useRouter();
  const { user, clearAuth } = useAuthStore();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleOutsideClick(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  const handleLogout = () => {
    setDropdownOpen(false);
    clearAuth();
    router.push('/login');
  };

  const handleProfile = () => {
    setDropdownOpen(false);
    router.push('/profile');
  };

  const handleSettings = () => {
    setDropdownOpen(false);
    router.push('/settings');
  };

  return (
    <header className="fixed top-0 right-0 left-20 z-30 flex items-center justify-between px-6 py-3 bg-[var(--aiko-surface)]/80 backdrop-blur-md border-b border-[var(--aiko-border)]">
      {/* Left — page title */}
      <div className="flex items-center gap-3">
        {title && (
          <h1 className="text-sm font-semibold text-[var(--aiko-text)]">{title}</h1>
        )}
      </div>

      {/* Right — trial badge + user profile */}
      <div className="flex items-center gap-3 ml-auto">
        {/* Trial / Free badge */}
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/25 select-none">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-xs font-medium text-amber-400">Free Version</span>
        </div>

        {/* User profile dropdown */}
        <div ref={dropdownRef} className="relative">
          <button
            onClick={() => setDropdownOpen((prev) => !prev)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[var(--aiko-surface-2)] border border-[var(--aiko-border)] hover:border-[var(--aiko-pink)]/40 transition-colors group"
          >
            {/* Avatar */}
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[var(--aiko-pink)] to-[var(--aiko-purple)] flex items-center justify-center text-white font-semibold text-xs flex-shrink-0">
              {user?.username?.charAt(0).toUpperCase() ?? 'A'}
            </div>

            {/* Username */}
            <span className="text-sm text-[var(--aiko-text)] font-medium hidden sm:block max-w-[120px] truncate">
              {user?.username ?? 'Guest'}
            </span>

            <ChevronDown
              className={[
                'w-4 h-4 text-[var(--aiko-text-muted)] transition-transform duration-200',
                dropdownOpen ? 'rotate-180' : '',
              ].join(' ')}
            />
          </button>

          {/* Dropdown menu */}
          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 rounded-xl bg-[var(--aiko-surface-2)] border border-[var(--aiko-border)] shadow-xl shadow-black/40 overflow-hidden py-1 z-50">
              {/* User info */}
              <div className="px-4 py-2.5 border-b border-[var(--aiko-border)]">
                <p className="text-sm font-medium text-[var(--aiko-text)] truncate">
                  {user?.username ?? 'Guest'}
                </p>
                <p className="text-xs text-[var(--aiko-text-muted)] truncate">
                  {user?.email ?? ''}
                </p>
              </div>

              <button
                onClick={handleProfile}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-[var(--aiko-text-muted)] hover:bg-[var(--aiko-border)] hover:text-[var(--aiko-text)] transition-colors"
              >
                <User className="w-4 h-4" />
                Profile
              </button>

              <button
                onClick={handleSettings}
                className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-[var(--aiko-text-muted)] hover:bg-[var(--aiko-border)] hover:text-[var(--aiko-text)] transition-colors"
              >
                <Settings className="w-4 h-4" />
                Settings
              </button>

              <div className="border-t border-[var(--aiko-border)] mt-1 pt-1">
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-rose-400 hover:bg-rose-500/10 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
