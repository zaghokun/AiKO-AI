'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { 
  LogOut, 
  User,
  Trash2,
  Edit,
  Settings,
  Menu,
  X
} from 'lucide-react';
import { useAuthStore } from '@/lib/store';
import { Button } from '@/components/ui/button';

export function Sidebar() {
  const router = useRouter();
  const { clearAuth } = useAuthStore();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    clearAuth();
    router.push('/login');
  };

  const handleProfile = () => {
    router.push('/profile');
  };

  const handleSettings = () => {
    router.push('/settings');
  };

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="fixed left-4 top-4 z-50 rounded-xl border border-cyan-300/30 bg-[#0f162b]/80 p-2 text-cyan-100 backdrop-blur-md transition-colors hover:bg-[#1a2440] lg:hidden"
      >
        {isMobileMenuOpen ? (
          <X className="h-5 w-5" />
        ) : (
          <Menu className="h-5 w-5" />
        )}
      </button>

      {/* Overlay */}
      {isMobileMenuOpen && (
        <div
          onClick={() => setIsMobileMenuOpen(false)}
          className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-0 h-screen bg-transparent
          transition-transform duration-300 z-40
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 w-20
        `}
      >
        <div className="flex h-full flex-col py-4">
          {/* Menu Icons */}
          <nav className="flex flex-1 flex-col items-center justify-center space-y-3 px-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleProfile}
              className="h-11 w-11 rounded-xl text-slate-400 transition-colors hover:bg-white/10 hover:text-cyan-200"
              title="Profile"
            >
              <User className="h-5 w-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="h-11 w-11 rounded-xl text-slate-400 transition-colors hover:bg-white/10 hover:text-cyan-200"
              title="Clear Chat"
            >
              <Trash2 className="h-5 w-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="h-11 w-11 rounded-xl text-slate-400 transition-colors hover:bg-white/10 hover:text-cyan-200"
              title="Edit"
            >
              <Edit className="h-5 w-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={handleSettings}
              className="h-11 w-11 rounded-xl text-slate-400 transition-colors hover:bg-white/10 hover:text-cyan-200"
              title="Settings"
            >
              <Settings className="h-5 w-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
              className="h-11 w-11 rounded-xl text-slate-400 transition-colors hover:bg-rose-500/15 hover:text-rose-300"
              title="Logout"
            >
              <LogOut className="h-5 w-5" />
            </Button>
          </nav>
        </div>
      </aside>
    </>
  );
}
