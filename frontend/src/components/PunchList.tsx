"use client";

import type { PunchItem } from "@/lib/api";

const STATUS_LABELS: Record<PunchItem["status"], string> = {
  open: "باز",
  in_progress: "در حال اصلاح",
  closed: "بسته‌شده",
};

/** لیست punch (issue #23) — نمای وب برای مکمل اپ موبایل ثبت ایراد (issue #22). */
export function PunchList({ items }: { items: PunchItem[] }) {
  if (items.length === 0) {
    return <p style={{ color: "var(--muted)" }}>هیچ آیتم punch list ای ثبت نشده است.</p>;
  }

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr style={{ textAlign: "right", color: "var(--muted)", fontSize: 13 }}>
          <th style={{ padding: 8 }}>شناسه ایراد</th>
          <th style={{ padding: 8 }}>وضعیت</th>
          <th style={{ padding: 8 }}>تاریخ بسته‌شدن</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id} className="card" style={{ display: "table-row" }}>
            <td style={{ padding: 8 }}>{item.defect_id.slice(0, 8)}</td>
            <td style={{ padding: 8 }}>{STATUS_LABELS[item.status]}</td>
            <td style={{ padding: 8 }}>{item.closed_at ?? "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
