"use client";

import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import { useEffect, useState } from "react";
import { getResultsPaged, exportResultUrl, getMe, getHistoryPaged } from "@/lib/api";

type HistoryRow = { id: number; user_id: number; action: string; meta_json: Record<string, unknown> };
type ResultRow = { id: number; summary: string; scores: { score: number }; created_by: string };

export default function ReportsPage() {
  const [rows, setRows] = useState<HistoryRow[]>([]);
  const [results, setResults] = useState<ResultRow[]>([]);
  const [action, setAction] = useState<string>("");
  const [mine, setMine] = useState<boolean>(false);
  const [histTotal, setHistTotal] = useState<number>(0);
  const [resTotal, setResTotal] = useState<number>(0);
  const [histOffset, setHistOffset] = useState<number>(0);
  const [resOffset, setResOffset] = useState<number>(0);

  useEffect(() => {
    getHistoryPaged<HistoryRow>(20, histOffset, action)
      .then(({ items, total }) => { setRows(items); setHistTotal(total); })
      .catch(() => { setRows([]); setHistTotal(0); });
    getResultsPaged<ResultRow>(10, resOffset, mine)
      .then(({ items, total }) => { setResults(items); setResTotal(total); })
      .catch(() => { setResults([]); setResTotal(0); });
  }, [action, mine, histOffset, resOffset]);

  useEffect(() => {
    getMe().then((m) => {
      const s = typeof m?.sub === "string" ? m.sub : null;
      if (s) setMine(true);
    }).catch(() => {});
  }, []);
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-4 space-y-4">
          <h1 className="text-xl font-semibold">Reports</h1>
          <div className="flex items-center gap-2 text-sm">
            <label>Filter action:</label>
            <select className="border rounded px-2 py-1 bg-transparent" value={action} onChange={(e) => setAction(e.target.value)}>
              <option value="">All</option>
              <option value="analysis_run">analysis_run</option>
              <option value="analysis_stored">analysis_stored</option>
            </select>
            <label className="ml-4 inline-flex items-center gap-1"><input type="checkbox" checked={mine} onChange={(e) => setMine(e.target.checked)} /> Mine only</label>
          </div>
          <div className="border border-black/10 dark:border-white/10 rounded-md p-4">
            <div className="flex items-center justify-between mb-2 text-sm opacity-70">
              <span>History: {rows.length} / {histTotal}</span>
              <div className="space-x-2">
                <button className="px-2 py-0.5 border rounded disabled:opacity-50" disabled={histOffset<=0} onClick={()=>setHistOffset(Math.max(0, histOffset-20))}>Prev</button>
                <button className="px-2 py-0.5 border rounded disabled:opacity-50" disabled={histOffset+20>=histTotal} onClick={()=>setHistOffset(histOffset+20)}>Next</button>
              </div>
            </div>
            <ul className="space-y-2 text-sm">
              {rows.map((r) => (
                <li key={r.id} className="flex items-center justify-between">
                  <span>#{r.id} — {r.action}</span>
                  <span className="opacity-70">{
                    (() => {
                      const v = (r.meta_json as { result_id?: unknown }).result_id;
                      return typeof v === "string" ? v : typeof v === "number" ? String(v) : "";
                    })()
                  }</span>
                </li>
              ))}
              {rows.length === 0 ? (
                <li className="opacity-70">No history yet.</li>
              ) : null}
            </ul>
          </div>
          <div className="border border-black/10 dark:border-white/10 rounded-md p-4">
            <div className="flex items-center justify-between mb-2 text-sm opacity-70">
              <span>Results: {results.length} / {resTotal}</span>
              <div className="space-x-2">
                <button className="px-2 py-0.5 border rounded disabled:opacity-50" disabled={resOffset<=0} onClick={()=>setResOffset(Math.max(0, resOffset-10))}>Prev</button>
                <button className="px-2 py-0.5 border rounded disabled:opacity-50" disabled={resOffset+10>=resTotal} onClick={()=>setResOffset(resOffset+10)}>Next</button>
              </div>
            </div>
            <h2 className="font-semibold mb-2">Recent Results</h2>
            <ul className="space-y-2 text-sm">
              {results.map((r) => (
                <li key={r.id} className="flex items-center justify-between">
                  <span>#{r.id} — {r.summary}</span>
                  <span className="space-x-3">
                    <a className="underline" href={exportResultUrl(r.id, "json")} target="_blank" rel="noreferrer">Export JSON</a>
                    <a className="underline" href={exportResultUrl(r.id, "csv")} target="_blank" rel="noreferrer">Export CSV</a>
                  </span>
                </li>
              ))}
              {results.length === 0 ? (
                <li className="opacity-70">No results.</li>
              ) : null}
            </ul>
          </div>
        </main>
      </div>
    </div>
  );
}


