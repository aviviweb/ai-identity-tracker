"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 border-r border-black/10 dark:border-white/10 p-4 space-y-3">
      <div className="text-xs uppercase tracking-wide opacity-60">Navigation</div>
      <nav className="flex flex-col gap-2 text-sm">
        <Link href="/dashboard" className="hover:underline">Dashboard</Link>
        <Link href="/reports" className="hover:underline">Reports</Link>
      </nav>
    </aside>
  );
}


