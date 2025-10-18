export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";

export async function apiFetch(path: string, init: RequestInit = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`,
    {
      ...init,
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        ...(init.headers || {}),
      },
    }
  );
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return res.json();
  return res.text();
}

export async function login(email: string, password: string) {
  return apiFetch("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
}

export async function getDemoProfiles(mode: "demo" | "live") {
  const search = new URLSearchParams({ mode }).toString();
  return apiFetch(`/profiles?${search}`);
}

export async function runAnalysis(subjectIds: string[], textGroups: string[][], imageUrls: string[]) {
  return apiFetch(`/analysis/run`, {
    method: "POST",
    body: JSON.stringify({ subject_ids: subjectIds, text_groups: textGroups, image_urls: imageUrls }),
  });
}

export async function getHistory(limit = 20) {
  const search = new URLSearchParams({ limit: String(limit) }).toString();
  return apiFetch(`/history?${search}`);
}

export async function getHistoryPaged<T = unknown>(limit = 20, offset = 0, action = ""): Promise<{ items: T[]; total: number }> {
  const qs = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (action) qs.set("action", action);
  const res = await fetch(`${API_BASE_URL}/history?${qs.toString()}`, { credentials: "include" });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  const total = Number(res.headers.get("X-Total-Count") || "0");
  const items: T[] = await res.json();
  return { items, total };
}

export async function getResults(limit = 20, mine = false) {
  const search = new URLSearchParams({ limit: String(limit), mine: mine ? "1" : "0" }).toString();
  return apiFetch(`/results?${search}`);
}

export async function getResult(id: number) {
  return apiFetch(`/results/${id}`);
}

export function exportResultUrl(id: number, format: "json" | "csv" = "json") {
  const p = new URLSearchParams({ format }).toString();
  return `${API_BASE_URL}/results/${id}/export?${p}`;
}

export async function getMe() {
  return apiFetch(`/auth/me`);
}

export async function getResultsPaged<T = unknown>(limit = 20, offset = 0, mine = false): Promise<{ items: T[]; total: number }> {
  const qs = new URLSearchParams({ limit: String(limit), offset: String(offset), mine: mine ? "1" : "0" });
  const res = await fetch(`${API_BASE_URL}/results?${qs.toString()}`, { credentials: "include" });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  const total = Number(res.headers.get("X-Total-Count") || "0");
  const items: T[] = await res.json();
  return { items, total };
}


