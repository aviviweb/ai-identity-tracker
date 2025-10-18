"use client";

import { useState } from "react";
import Link from "next/link";
import { login } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      window.location.href = "/dashboard";
    } catch {
      setError("Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen grid place-items-center p-6">
      <div className="w-full max-w-sm border border-black/10 dark:border-white/10 rounded-md p-6 bg-background">
        <h1 className="text-lg font-semibold mb-4">Login</h1>
        <form onSubmit={onSubmit} className="space-y-3">
          <div className="space-y-1">
            <label className="text-sm">Email</label>
            <input
              className="w-full border rounded px-2 py-1 bg-transparent"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm">Password</label>
            <input
              className="w-full border rounded px-2 py-1 bg-transparent"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button
            className="w-full h-10 rounded bg-foreground text-background disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "..." : "Login"}
          </button>
        </form>
        <div className="mt-3 text-sm opacity-70">
          <Link href="/">Back</Link>
        </div>
      </div>
    </div>
  );
}


