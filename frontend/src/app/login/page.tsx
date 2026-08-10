"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

/** صفحه‌ی ورود — احراز هویت (issue #7). */
export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const { access_token } = await api.login(email, password);
      window.localStorage.setItem("sakhtban_token", access_token);
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "خطای ناشناخته");
    }
  }

  return (
    <main className="container" style={{ maxWidth: 420 }}>
      <h1>ورود</h1>
      <form onSubmit={handleSubmit} className="grid">
        <input
          type="email"
          placeholder="ایمیل"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="رمز عبور"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
        <button type="submit">ورود</button>
      </form>
    </main>
  );
}
