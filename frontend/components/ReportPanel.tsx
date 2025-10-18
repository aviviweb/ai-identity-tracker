"use client";

import { useEffect, useState } from "react";
import { apiFetch, runAnalysis, exportResultUrl } from "@/lib/api";
import type { DemoProfile } from "@/types/demo";

type Props = {
  profiles: DemoProfile[];
  onComponentsUpdate?: (c: { style: number; image: number } | null) => void;
};

export default function ReportPanel({ profiles, onComponentsUpdate }: Props) {
  const [summary, setSummary] = useState<string>("");
  const [score, setScore] = useState<number | null>(null);
  const [label, setLabel] = useState<string>("");
  const [components, setComponents] = useState<{ style: number; image: number } | null>(null);
  const [saving, setSaving] = useState(false);
  const [resultId, setResultId] = useState<number | null>(null);
  const [toast, setToast] = useState<string>("");

  useEffect(() => {
    async function run() {
      if (!profiles || profiles.length < 2) return;
      const texts: string[][] = profiles.map((p): string[] => p.sample_posts?.posts ?? []);
      const images = profiles
        .map((p) => p.avatar_url)
        .filter((u): u is string => Boolean(u));
      try {
        const res = await apiFetch("/analysis/correlate", {
          method: "POST",
          body: JSON.stringify({ text_groups: texts, image_urls: images }),
        });
        setSummary(res.summary ?? JSON.stringify(res));
        setScore(res.score ?? null);
        setLabel(res.label ?? "");
        setComponents(res.components ?? null);
        setResultId(typeof res.id === "number" ? res.id : null);
        onComponentsUpdate?.(res.components ?? null);
      } catch {
        setSummary("");
        setScore(null);
        setLabel("");
        setComponents(null);
        setResultId(null);
        onComponentsUpdate?.(null);
      }
    }
    run();
  }, [profiles, onComponentsUpdate]);

  return (
    <div className="border border-black/10 dark:border-white/10 rounded-md p-4">
      <h2 className="font-semibold mb-2">AI Report</h2>
      <div className="mb-3">
        <button
          className="h-9 px-3 rounded bg-foreground text-background text-sm disabled:opacity-50"
          disabled={saving || profiles.length < 2}
          onClick={async () => {
            if (!profiles || profiles.length < 2) return;
            const texts: string[][] = profiles.map((p): string[] => p.sample_posts?.posts ?? []);
            const images = profiles
              .map((p) => p.avatar_url)
              .filter((u): u is string => Boolean(u));
            const ids = profiles.map((p) => String(p.id));
            try {
              setSaving(true);
              const res = await runAnalysis(ids, texts, images);
              setSummary(res.summary ?? "");
              setScore(res.score ?? null);
              setLabel(res.label ?? "");
              const comp = res.components ?? null;
              setComponents(comp);
              setResultId(typeof res.id === "number" ? res.id : null);
              onComponentsUpdate?.(comp);
              // Show toast and then redirect to Reports page
              setToast("Analysis saved");
              try { setTimeout(() => { try { window.location.href = "/reports" } catch {} }, 800) } catch {}
            } finally {
              setSaving(false);
            }
          }}
        >
          {saving ? "Running..." : "Run analysis"}
        </button>
      </div>
      {summary ? (
        <p className="text-sm leading-6">{summary}</p>
      ) : (
        <p className="text-sm opacity-70">No report yet.</p>
      )}
      {typeof score === "number" ? (
        <div className="mt-3">
          <div className="flex items-center justify-between text-sm">
            <div>
              Identity Confidence: <span className="font-semibold">{Math.round(score * 100)}%</span>
            </div>
            {label ? (
              <span
                className={
                  "ml-2 inline-block px-2 py-0.5 rounded text-xs capitalize " +
                  (label === "high"
                    ? "bg-green-500/15 text-green-700 dark:text-green-300"
                    : label === "medium"
                    ? "bg-yellow-500/15 text-yellow-700 dark:text-yellow-300"
                    : "bg-red-500/15 text-red-700 dark:text-red-300")
                }
              >
                {label}
              </span>
            ) : null}
          </div>
          <div className="mt-2 h-2 w-full rounded bg-black/5 dark:bg-white/10 overflow-hidden">
            <div
              className="h-full bg-blue-500 dark:bg-blue-400"
              style={{ width: `${Math.round(score * 100)}%` }}
            />
          </div>
        </div>
      ) : null}
      {components ? (
        <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
          <div className="opacity-80">Style: <span className="font-semibold">{Math.round(components.style * 100)}%</span></div>
          <div className="opacity-80">Image: <span className="font-semibold">{Math.round(components.image * 100)}%</span></div>
        </div>
      ) : null}
      {resultId !== null ? (
        <div className="mt-3 text-sm">
          <a className="underline" href={exportResultUrl(resultId)} target="_blank" rel="noreferrer">Export result</a>
        </div>
      ) : null}
      {toast ? (
        <div className="fixed bottom-4 right-4 px-3 py-2 rounded bg-black/80 text-white text-sm shadow-lg">
          {toast}
        </div>
      ) : null}
    </div>
  );
}


