"use client";

import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import DemoToggle from "@/components/DemoToggle";
import ChartsPanel from "@/components/ChartsPanel";
import { getDemoProfiles } from "@/lib/api";
import { useEffect, useState } from "react";
import ReportPanel from "@/components/ReportPanel";
import type { DemoProfile } from "@/types/demo";

export default function DashboardPage() {
  const [profiles, setProfiles] = useState<DemoProfile[]>([]);
  const [mode, setMode] = useState<"demo" | "live">("demo");
  const [components, setComponents] = useState<{ style: number; image: number } | null>(null);

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem("demoMode");
      if (stored !== null) setMode(stored === "true" ? "demo" : "live");
    } catch {}
  }, []);

  useEffect(() => {
    getDemoProfiles(mode).then(setProfiles).catch(() => setProfiles([]));
  }, [mode]);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-4 space-y-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold">Dashboard</h1>
            <DemoToggle />
          </div>
          <ChartsPanel components={components ?? undefined} />
          <section className="border border-black/10 dark:border-white/10 rounded-md p-4">
            <h2 className="font-semibold mb-2">Demo Profiles</h2>
            <ul className="space-y-2 text-sm">
              {profiles.map((p) => (
                <li key={p.id} className="flex items-center justify-between">
                  <span>{p.platform} — {p.handle} — {p.display_name}</span>
                </li>
              ))}
              {profiles.length === 0 ? (
                <li className="opacity-70">No profiles.</li>
              ) : null}
            </ul>
          </section>
          <ReportPanel profiles={profiles} onComponentsUpdate={setComponents} />
        </main>
      </div>
    </div>
  );
}


