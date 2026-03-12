'use client';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';
import { Heart, User } from 'lucide-react';

interface MessageBubbleProps {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  memoriesUsed?: number;
}

export function MessageBubble({ role, content, timestamp, memoriesUsed }: MessageBubbleProps) {
  const isUser = role === 'user';
  const isSystem = role === 'system';

  if (isSystem) {
    return (
      <div className="flex justify-center my-4">
        <div className="px-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-full text-xs text-gray-600 dark:text-gray-400">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className={cn('flex gap-3 mb-4', isUser ? 'flex-row-reverse' : 'flex-row')}>
      {/* Avatar */}
      <Avatar className={cn('w-8 h-8 flex-shrink-0', isUser ? 'bg-violet-500' : 'bg-pink-500')}>
        <AvatarFallback className="text-white">
          {isUser ? <User className="w-4 h-4" /> : <Heart className="w-4 h-4 fill-white" />}
        </AvatarFallback>
      </Avatar>

      {/* Message Content */}
      <div className={cn('flex flex-col', isUser ? 'items-end' : 'items-start', 'max-w-[70%]')}>
        <div
          className={cn(
            'px-4 py-2 rounded-2xl',
            isUser
              ? 'bg-gradient-to-r from-violet-500 to-purple-500 text-white'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
          )}
        >
          <p className="text-sm whitespace-pre-wrap break-words">{content}</p>
        </div>

        {/* Timestamp & Info */}
        <div className="flex items-center gap-2 mt-1 px-1">
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {formatDistanceToNow(new Date(timestamp), { addSuffix: true })}
          </span>
          {!isUser && memoriesUsed !== undefined && memoriesUsed > 0 && (
            <span className="text-xs text-violet-500 dark:text-violet-400">
              • {memoriesUsed} {memoriesUsed === 1 ? 'memory' : 'memories'}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
