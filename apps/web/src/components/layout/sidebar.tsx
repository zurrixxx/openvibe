"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { trpc } from "@/lib/trpc";
import { useWorkspaceStore } from "@/lib/stores/workspace-store";

export function Sidebar() {
  const pathname = usePathname();
  const workspaceId = useWorkspaceStore((s) => s.workspaceId);
  const workspaceName = useWorkspaceStore((s) => s.workspaceName);

  const { data: channels } = trpc.channel.list.useQuery(
    { workspaceId: workspaceId! },
    { enabled: !!workspaceId }
  );

  const initial = (workspaceName ?? "O").charAt(0).toUpperCase();

  return (
    <aside className="flex w-60 flex-col border-r border-border bg-sidebar">
      {/* Workspace header */}
      <div className="flex h-12 items-center gap-2.5 border-b border-border px-4">
        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-primary text-xs font-bold text-primary-foreground">
          {initial}
        </div>
        <h1 className="truncate text-sm font-semibold text-foreground">
          {workspaceName ?? "OpenVibe"}
        </h1>
      </div>

      {/* Channel list */}
      <nav className="flex-1 overflow-y-auto px-2 py-3">
        <div className="mb-1.5 px-2 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          Channels
        </div>
        <ul className="space-y-px">
          {channels?.map((channel) => {
            const href = `/${channel.name}`;
            const isActive = pathname === href;

            return (
              <li key={channel.id}>
                <Link
                  href={href}
                  className={clsx(
                    "relative flex items-center rounded-md px-2 py-1 text-[13px] transition-colors",
                    isActive
                      ? "bg-sidebar-active-bg font-medium text-foreground"
                      : "text-sidebar-foreground hover:bg-sidebar-hover hover:text-foreground"
                  )}
                >
                  {isActive && (
                    <span className="absolute -left-2 top-1 bottom-1 w-0.5 rounded-full bg-primary" />
                  )}
                  <span
                    className={clsx(
                      "mr-1.5 text-xs",
                      isActive ? "text-primary" : "text-muted-foreground"
                    )}
                  >
                    #
                  </span>
                  {channel.name}
                </Link>
              </li>
            );
          })}
          {!channels && (
            <li className="px-2 py-1 text-[13px] text-muted-foreground">Loading...</li>
          )}
        </ul>
      </nav>
    </aside>
  );
}
