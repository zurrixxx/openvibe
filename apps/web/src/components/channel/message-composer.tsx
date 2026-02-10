"use client";

import { useState, useRef, useCallback } from "react";
import { trpc } from "@/lib/trpc";

interface MessageComposerProps {
  channelId: string;
  channelName: string;
}

export function MessageComposer({
  channelId,
  channelName,
}: MessageComposerProps) {
  const [content, setContent] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const utils = trpc.useUtils();

  const sendMessage = trpc.message.send.useMutation({
    onSuccess: () => {
      setContent("");
      utils.message.list.invalidate({ channelId });
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    },
  });

  const handleSubmit = useCallback(() => {
    const trimmed = content.trim();
    if (!trimmed || sendMessage.isPending) return;
    sendMessage.mutate({ channelId, content: trimmed });
  }, [content, channelId, sendMessage]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
    // Auto-resize
    const el = e.target;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";
  };

  return (
    <div className="px-4 pb-4 pt-2">
      <div className="flex items-end rounded-lg border border-border bg-input px-3 py-2 transition-shadow focus-within:border-primary/50 focus-within:shadow-[var(--shadow-glow-primary)]">
        <textarea
          ref={textareaRef}
          value={content}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={`Message #${channelName}`}
          rows={1}
          className="max-h-[200px] flex-1 resize-none bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none"
        />
        <button
          onClick={handleSubmit}
          disabled={!content.trim() || sendMessage.isPending}
          className="ml-2 rounded-md p-1.5 text-secondary transition-colors hover:bg-hover hover:text-foreground disabled:opacity-30"
        >
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 12h14M12 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}
