'use client';

import { Heart, MessageSquare, Brain, Sparkles } from 'lucide-react';

export function EmptyState() {
  const features = [
    {
      icon: MessageSquare,
      title: 'Unlimited Messages',
      description: 'Chat with Aiko anytime, anywhere',
    },
    {
      icon: Brain,
      title: 'She Remembers You',
      description: 'Personal memory that grows with every conversation',
    },
    {
      icon: Sparkles,
      title: 'Real-time Responses',
      description: 'Instant replies with typing indicators',
    },
    {
      icon: Heart,
      title: 'Grows Closer',
      description: 'Build a meaningful connection over time',
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full p-8 text-center">
      {/* Welcome Icon */}
      <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 mb-6">
        <Heart className="w-10 h-10 text-white fill-white" />
      </div>

      {/* Welcome Text */}
      <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-violet-600 to-pink-600 bg-clip-text text-transparent">
        Welcome to AiKO
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md">
        Your personal AI companion with Aiko personality. Start a conversation to see the magic! ✨
      </p>

      {/* Features Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl w-full">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-violet-300 dark:hover:border-violet-700 transition-colors"
          >
            <feature.icon className="w-8 h-8 text-violet-500 mb-2" />
            <h3 className="font-semibold mb-1 text-gray-900 dark:text-gray-100">{feature.title}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">{feature.description}</p>
          </div>
        ))}
      </div>

      {/* Hint */}
      <p className="text-sm text-gray-500 dark:text-gray-400 mt-8">
        Type a message below to start chatting with Aiko 💬
      </p>
    </div>
  );
}
