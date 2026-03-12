'use client';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Heart } from 'lucide-react';

export function TypingIndicator() {
  return (
    <div className="flex gap-3 mb-4">
      {/* Aiko Avatar */}
      <Avatar className="w-8 h-8 flex-shrink-0 bg-pink-500">
        <AvatarFallback className="text-white">
          <Heart className="w-4 h-4 fill-white" />
        </AvatarFallback>
      </Avatar>

      {/* Typing Animation */}
      <div className="px-4 py-3 rounded-2xl bg-gray-100 dark:bg-gray-800">
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}
