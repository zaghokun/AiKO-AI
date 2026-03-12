'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Heart, 
  LogOut, 
  User,
  Trash2,
  Edit,
  Settings,
  Menu,
  X
} from 'lucide-react';
import { useAuthStore, useChatStore } from '@/lib/store';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';

export function Sidebar() {
  const router = useRouter();
  const { user, clearAuth } = useAuthStore();
  const { isConnected } = useChatStore();
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
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-gray-800/80 backdrop-blur-sm border border-gray-700 hover:bg-gray-700 transition-colors"
      >
        {isMobileMenuOpen ? (
          <X className="w-5 h-5 text-gray-300" />
        ) : (
          <Menu className="w-5 h-5 text-gray-300" />
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
          fixed left-0 top-0 h-screen bg-gray-900/95 backdrop-blur-sm border-r border-gray-800
          transition-transform duration-300 z-40
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 w-20
        `}
      >
        <div className="flex flex-col h-full py-4">
          {/* Profile Card at Top */}
          <div className="px-3 mb-6">
            <div className="relative">
              <Avatar className="w-14 h-14 mx-auto border-2 border-purple-500/50">
                <AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-500 text-white font-semibold text-lg">
                  {user?.username?.charAt(0).toUpperCase() || 'A'}
                </AvatarFallback>
              </Avatar>
              
              {/* Online Status Indicator */}
              <div className="absolute bottom-0 right-1/2 translate-x-1/2 translate-y-1">
                <div
                  className={`w-3 h-3 rounded-full border-2 border-gray-900 ${
                    isConnected ? 'bg-green-500' : 'bg-red-500'
                  }`}
                />
              </div>
            </div>
            
            {/* Username */}
            <div className="mt-2 text-center">
              <p className="text-xs text-gray-400 font-medium truncate">
                {user?.username || 'Guest'}
              </p>
              <p className={`text-[10px] ${isConnected ? 'text-green-500' : 'text-red-500'}`}>
                {isConnected ? 'Online' : 'Offline'}
              </p>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-800 mb-4" />

          {/* Menu Icons */}
          <nav className="flex-1 flex flex-col items-center space-y-2 px-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleProfile}
              className="w-12 h-12 rounded-xl hover:bg-gray-800 text-gray-400 hover:text-purple-400 transition-colors"
              title="Profile"
            >
              <User className="w-5 h-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="w-12 h-12 rounded-xl hover:bg-gray-800 text-gray-400 hover:text-purple-400 transition-colors"
              title="Clear Chat"
            >
              <Trash2 className="w-5 h-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="w-12 h-12 rounded-xl hover:bg-gray-800 text-gray-400 hover:text-purple-400 transition-colors"
              title="Edit"
            >
              <Edit className="w-5 h-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={handleSettings}
              className="w-12 h-12 rounded-xl hover:bg-gray-800 text-gray-400 hover:text-purple-400 transition-colors"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </Button>
          </nav>

          {/* Divider */}
          <div className="border-t border-gray-800 mt-4 mb-4" />

          {/* Logout Button at Bottom */}
          <div className="px-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
              className="w-12 h-12 rounded-xl hover:bg-red-500/10 text-gray-400 hover:text-red-400 transition-colors"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </aside>
    </>
  );
}
