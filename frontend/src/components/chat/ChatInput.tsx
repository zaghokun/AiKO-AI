'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Paperclip, Image as ImageIcon } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSend, disabled = false, placeholder = 'Type a message...' }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="glass-panel rounded-2xl border border-white/10 p-3">
      <div className="flex items-center gap-2">
        {/* Upload Buttons */}
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="h-10 w-10 flex-shrink-0 rounded-xl text-slate-400 hover:bg-white/10 hover:text-cyan-200"
          disabled={disabled}
          title="Upload image (coming soon)"
        >
          <ImageIcon className="w-5 h-5" />
        </Button>

        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="h-10 w-10 flex-shrink-0 rounded-xl text-slate-400 hover:bg-white/10 hover:text-cyan-200"
          disabled={disabled}
          title="Upload file (coming soon)"
        >
          <Paperclip className="w-5 h-5" />
        </Button>

        {/* Message Input */}
        <Input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className="h-11 flex-1 rounded-xl border-white/10 bg-[#10192e]/70 text-slate-100 placeholder:text-slate-500 focus-visible:ring-cyan-400/50"
          autoComplete="off"
        />

        {/* Send Button */}
        <Button
          type="submit"
          size="icon"
          disabled={disabled || !message.trim()}
          className="h-11 w-11 flex-shrink-0 rounded-xl border border-cyan-200/30 bg-gradient-to-br from-fuchsia-500 to-cyan-500 text-white hover:brightness-110"
        >
          <Send className="w-5 h-5" />
        </Button>
      </div>
    </form>
  );
}
