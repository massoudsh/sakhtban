"use client";

import { useState } from "react";
import { api } from "@/lib/api";

/** فرم ثبت گزارش هفتگی/روزانه از کانال وب (issue #6) — متن آزاد پارس‌شده با NLP (issue #2). */
export default function ReportsPage({ params }: { params: { projectId: string } }) {
  const [rawText, setRawText] = useState("");
  const [reportDate, setReportDate] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "error">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("sending");
    try {
      await api.submitReport(params.projectId, rawText, reportDate);
      setStatus("sent");
      setRawText("");
    } catch {
      setStatus("error");
    }
  }

  return (
    <main className="container" style={{ maxWidth: 560 }}>
      <h1>ثبت گزارش کارگاه</h1>
      <form onSubmit={handleSubmit} className="grid">
        <input type="date" value={reportDate} onChange={(e) => setReportDate(e.target.value)} required />
        <textarea
          rows={8}
          placeholder="مثلاً: امروز در طبقه ۳ بتن‌ریزی سقف انجام شد. ۵۰ متر مکعب بتن مصرف شد. به‌دلیل بارش باران کار متوقف شد."
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          required
        />
        <button type="submit" disabled={status === "sending"}>
          {status === "sending" ? "در حال ارسال..." : "ارسال گزارش"}
        </button>
        {status === "sent" && <p style={{ color: "var(--accent)" }}>گزارش ثبت و پردازش شد.</p>}
        {status === "error" && <p style={{ color: "var(--danger)" }}>ارسال گزارش ناموفق بود.</p>}
      </form>
    </main>
  );
}
