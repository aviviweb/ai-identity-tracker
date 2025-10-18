"use client";

import { useEffect, useState } from "react";

export default function DemoToggle() {
  const [demoMode, setDemoMode] = useState<boolean>(true);

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem("demoMode");
      if (stored !== null) setDemoMode(stored === "true");
    } catch {}
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem("demoMode", String(demoMode));
    } catch {}
  }, [demoMode]);

  return (
    <label className="inline-flex items-center gap-2 text-sm cursor-pointer select-none">
      <input
        type="checkbox"
        checked={demoMode}
        onChange={(e) => setDemoMode(e.target.checked)}
      />
      <span>Demo Mode</span>
    </label>
  );
}


