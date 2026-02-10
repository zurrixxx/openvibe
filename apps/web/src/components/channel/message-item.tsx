"use client";

import clsx from "clsx";

interface MessageItemProps {
  id: string;
  content: string;
  authorName: string | null;
  authorType: string;
  avatarUrl?: string | null;
  createdAt: string;
  isGrouped?: boolean;
}

export function MessageItem({
  content,
  authorName,
  authorType,
  createdAt,
  isGrouped = false,
}: MessageItemProps) {
  const time = new Date(createdAt).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  const displayName = authorName ?? "Unknown";
  const isAgent = authorType === "agent";

  // Grouped message: compact layout, no avatar/name, timestamp on hover
  if (isGrouped) {
    return (
      <div
        className={clsx(
          "group flex gap-3 px-4 py-0.5 transition-colors hover:bg-hover",
          isAgent && "border-l-2 border-primary/40 bg-agent"
        )}
      >
        {/* Timestamp gutter — visible on hover, same width as avatar */}
        <div className="flex w-9 shrink-0 items-center justify-end">
          <span className="text-[10px] text-secondary opacity-0 transition-opacity group-hover:opacity-100">
            {time}
          </span>
        </div>
        <div className="min-w-0 flex-1">
          <div className="whitespace-pre-wrap text-sm leading-relaxed text-foreground">
            {content}
          </div>
        </div>
      </div>
    );
  }

  // Full message: avatar + name + timestamp
  return (
    <div
      className={clsx(
        "group flex gap-3 px-4 pt-3 pb-1 transition-colors hover:bg-hover",
        isAgent && "border-l-2 border-primary/40 bg-agent"
      )}
    >
      {/* Avatar */}
      <div
        className={clsx(
          "flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-semibold",
          isAgent
            ? "bg-primary-muted text-primary"
            : "bg-elevated text-secondary"
        )}
      >
        {isAgent ? "AI" : displayName.charAt(0).toUpperCase()}
      </div>

      {/* Content */}
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline gap-2">
          <span className="text-sm font-semibold text-foreground">
            {displayName}
          </span>
          {isAgent && (
            <span className="rounded bg-primary-muted px-1.5 py-0.5 text-[10px] font-medium text-primary">
              BOT
            </span>
          )}
          <span className="text-[11px] text-secondary">{time}</span>
        </div>
        <div className="mt-0.5 whitespace-pre-wrap text-sm leading-relaxed text-foreground">
          {content}
        </div>
      </div>
    </div>
  );
}
