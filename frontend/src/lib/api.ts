/** کلاینت سبک fetch برای ارتباط با Sakhtban API (بدون وابستگی به کتابخانه‌ی سنگین). */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("sakhtban_token");
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`درخواست ناموفق (${res.status}): ${body}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export interface RiskItem {
  id: string;
  source_type: "schedule_deviation" | "cost_deviation" | "decision_ambiguity" | "qa_rework_pattern";
  title: string;
  location: string | null;
  severity_score: number;
  likelihood_score: number;
  is_resolved: boolean;
}

export interface Decision {
  id: string;
  statement: string;
  responsible_party: string | null;
  decision_date: string | null;
  status: string;
  financial_impact: number | null;
  ambiguity_flags: { ambiguity_type: string; explanation: string; risk_score: number }[];
}

export interface PunchItem {
  id: string;
  defect_id: string;
  status: "open" | "in_progress" | "closed";
  closed_at: string | null;
}

export interface ScheduleTask {
  id: string;
  external_task_id: string;
  name: string;
  wbs_path: string | null;
  baseline_finish: string | null;
  actual_finish: string | null;
  forecast_finish: string | null;
  percent_complete: number;
  status: "not_started" | "in_progress" | "completed";
}

export const api = {
  getRiskHeatmap: (projectId: string) => apiFetch<RiskItem[]>(`/risk-heatmap/${projectId}`),
  getDecisionTimeline: (projectId: string) => apiFetch<Decision[]>(`/decisions/${projectId}/timeline`),
  getPunchList: (projectId: string) => apiFetch<PunchItem[]>(`/qa/${projectId}/punch-list`),
  getScheduleTasks: (projectId: string) => apiFetch<ScheduleTask[]>(`/schedule/${projectId}/tasks`),
  submitReport: (projectId: string, rawText: string, reportDate: string) =>
    apiFetch(`/reports`, {
      method: "POST",
      body: JSON.stringify({ project_id: projectId, raw_text: rawText, report_date: reportDate, channel: "web" }),
    }),
  login: (email: string, password: string) =>
    apiFetch<{ access_token: string; token_type: string }>(`/auth/login`, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
};
