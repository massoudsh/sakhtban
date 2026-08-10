"use client";

import { useEffect, useState } from "react";
import { api, type PunchItem } from "@/lib/api";
import { PunchList } from "@/components/PunchList";

/** صفحه‌ی punch list — QA Copilot (issue #23). ثبت ایراد جدید از اپ موبایل انجام می‌شود (issue #22). */
export default function QaPage({ params }: { params: { projectId: string } }) {
  const [items, setItems] = useState<PunchItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getPunchList(params.projectId)
      .then(setItems)
      .catch((err) => setError(err instanceof Error ? err.message : "خطا در دریافت اطلاعات"))
      .finally(() => setLoading(false));
  }, [params.projectId]);

  return (
    <main className="container">
      <h1>Punch List</h1>
      {loading && <p style={{ color: "var(--muted)" }}>در حال بارگذاری...</p>}
      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      {!loading && !error && <PunchList items={items} />}
    </main>
  );
}
