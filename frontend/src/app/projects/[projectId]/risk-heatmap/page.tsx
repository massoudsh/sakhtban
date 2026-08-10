"use client";

import { useEffect, useState } from "react";
import { api, type RiskItem } from "@/lib/api";
import { RiskHeatmapGrid } from "@/components/RiskHeatmapGrid";

/** صفحه‌ی Risk Heatmap — نقطه‌ی اتصال هر سه لایه‌ی محصول (issue #4, #19, #25). */
export default function RiskHeatmapPage({ params }: { params: { projectId: string } }) {
  const [items, setItems] = useState<RiskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getRiskHeatmap(params.projectId)
      .then(setItems)
      .catch((err) => setError(err instanceof Error ? err.message : "خطا در دریافت اطلاعات"))
      .finally(() => setLoading(false));
  }, [params.projectId]);

  return (
    <main className="container">
      <h1>Risk Heatmap</h1>
      {loading && <p style={{ color: "var(--muted)" }}>در حال بارگذاری...</p>}
      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      {!loading && !error && <RiskHeatmapGrid items={items} />}
    </main>
  );
}
