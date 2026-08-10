"use client";

import { useEffect, useState } from "react";
import { api, type ScheduleTask } from "@/lib/api";

const STATUS_LABELS: Record<ScheduleTask["status"], string> = {
  not_started: "شروع‌نشده",
  in_progress: "در حال اجرا",
  completed: "تکمیل‌شده",
};

/** صفحه‌ی برنامه‌ی زمان‌بندی — نمایش فعالیت‌های import شده از Primavera/MS Project (issue #9, #10). */
export default function SchedulePage({ params }: { params: { projectId: string } }) {
  const [tasks, setTasks] = useState<ScheduleTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getScheduleTasks(params.projectId)
      .then(setTasks)
      .catch((err) => setError(err instanceof Error ? err.message : "خطا در دریافت اطلاعات"))
      .finally(() => setLoading(false));
  }, [params.projectId]);

  return (
    <main className="container">
      <h1>برنامه‌ی زمان‌بندی</h1>
      {loading && <p style={{ color: "var(--muted)" }}>در حال بارگذاری...</p>}
      {error && <p style={{ color: "var(--danger)" }}>{error}</p>}
      {!loading && !error && tasks.length === 0 && (
        <p style={{ color: "var(--muted)" }}>هنوز برنامه‌ی زمان‌بندی‌ای برای این پروژه import نشده است.</p>
      )}
      {!loading && !error && tasks.length > 0 && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ textAlign: "right", color: "var(--muted)", fontSize: 13 }}>
              <th style={{ padding: 8 }}>فعالیت</th>
              <th style={{ padding: 8 }}>پایان مبنا</th>
              <th style={{ padding: 8 }}>پایان واقعی/پیش‌بینی</th>
              <th style={{ padding: 8 }}>پیشرفت</th>
              <th style={{ padding: 8 }}>وضعیت</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((t) => (
              <tr key={t.id}>
                <td style={{ padding: 8 }}>{t.name}</td>
                <td style={{ padding: 8 }}>{t.baseline_finish ?? "—"}</td>
                <td style={{ padding: 8 }}>{t.actual_finish ?? t.forecast_finish ?? "—"}</td>
                <td style={{ padding: 8 }}>{t.percent_complete}%</td>
                <td style={{ padding: 8 }}>{STATUS_LABELS[t.status]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
