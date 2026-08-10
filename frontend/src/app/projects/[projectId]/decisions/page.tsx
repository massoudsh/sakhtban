"use client";

import { useEffect, useState } from "react";
import { api, type Decision } from "@/lib/api";
import { DecisionTimeline } from "@/components/DecisionTimeline";

/** صفحه‌ی خط زمانی تصمیم‌ها — Decision Log (issue #18). */
export default function DecisionsPage({ params }: { params: { projectId: string } }) {
  const [decisions, setDecisions] = useState<Decision[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getDecisionTimeline(params.projectId)
      .then(setDecisions)
      .catch((err) => setError(err instanceof Error ? err.message : "خطا در دریافت اطلاعات"))
      .finally(() => setLoading(false));
  }, [params.projectId]);

  return (
    <main className="container">
      <h1>خط زمانی تصمیم‌ها</h1>
      {loading && <p style={{ color: "var(--muted)" }}>در حال بارگذاری...</p>}
      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      {!loading && !error && <DecisionTimeline decisions={decisions} />}
    </main>
  );
}
