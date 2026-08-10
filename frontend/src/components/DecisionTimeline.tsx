"use client";

import type { Decision } from "@/lib/api";

/** خط زمانی تصمیم‌ها با نمایش پرچم ابهام (issue #18). */
export function DecisionTimeline({ decisions }: { decisions: Decision[] }) {
  if (decisions.length === 0) {
    return <p style={{ color: "var(--muted)" }}>هنوز تصمیمی از اسناد پروژه استخراج نشده است.</p>;
  }

  return (
    <div className="grid" style={{ gridTemplateColumns: "1fr" }}>
      {decisions.map((d) => (
        <div key={d.id} className="card">
          <div style={{ fontSize: 13, color: "var(--muted)" }}>
            {d.decision_date ?? "بدون تاریخ"} · {d.responsible_party ?? "مسئول نامشخص"} · وضعیت: {d.status}
          </div>
          <p style={{ margin: "8px 0" }}>{d.statement}</p>
          {d.ambiguity_flags.length > 0 && (
            <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 8 }}>
              {d.ambiguity_flags.map((f, i) => (
                <div key={i} style={{ color: "var(--danger)", fontSize: 13 }}>
                  ⚠ {f.explanation}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
