"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [demoMode, setDemoMode] = useState<boolean>(true);

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem("demoMode");
      if (stored !== null) {
        setDemoMode(stored === "true");
      }
    } catch {}
  }, []);

  return (
    <header className="w-full border-b border-black/10 dark:border-white/10 bg-background">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="font-semibold">
          AI Identity Tracker
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/reports">Reports</Link>
          <span className="opacity-70">Mode: {demoMode ? "Demo" : "Live"}</span>
        </nav>
      </div>
    </header>
  );
}


