"use client";

import type { RiskItem } from "@/lib/api";

/** رسم ساده‌ی Risk Heatmap (issue #4): محور severity/likelihood + رنگ بر اساس منبع ریسک. */
const SOURCE_LABELS: Record<RiskItem["source_type"], string> = {
  schedule_deviation: "انحراف زمان‌بندی",
  cost_deviation: "انحراف هزینه",
  decision_ambiguity: "ابهام تصمیم", // لایه‌ی دوم — Decision Log
  qa_rework_pattern: "الگوی rework", // لایه‌ی سوم — QA Copilot
};

const SOURCE_COLORS: Record<RiskItem["source_type"], string> = {
  schedule_deviation: "#e05d5d",
  cost_deviation: "#e0a15d",
  decision_ambiguity: "#5d8fe0",
  qa_rework_pattern: "#3fb6a8",
};

function severityLevel(score: number): string {
  if (score >= 75) return "بحرانی";
  if (score >= 50) return "بالا";
  if (score >= 25) return "متوسط";
  return "پایین";
}

export function RiskHeatmapGrid({ items }: { items: RiskItem[] }) {
  if (items.length === 0) {
    return <p style={{ color: "var(--muted)" }}>هیچ ریسک بازی در این پروژه ثبت نشده است.</p>;
  }

  const sorted = [...items].sort((a, b) => b.severity_score - a.severity_score);

  return (
    <div className="grid" style={{ gridTemplateColumns: "1fr" }}>
      {sorted.map((item) => (
        <div key={item.id} className="card" style={{ borderInlineStart: `4px solid ${SOURCE_COLORS[item.source_type]}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong>{item.title}</strong>
            <span style={{ color: SOURCE_COLORS[item.source_type], fontSize: 12 }}>
              {SOURCE_LABELS[item.source_type]}
            </span>
          </div>
          <div style={{ color: "var(--muted)", fontSize: 13, marginTop: 6 }}>
            {item.location && <span>موقعیت: {item.location} · </span>}
            شدت: {severityLevel(item.severity_score)} ({item.severity_score}) · احتمال: {item.likelihood_score}
          </div>
        </div>
      ))}
    </div>
  );
}
