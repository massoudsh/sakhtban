/**
 * کلاینت fetch برای Sakhtban API — نسخه‌ی موبایل (معادل frontend/src/lib/api.ts).
 * آدرس واقعی سرور بعد از استقرار باید در EXPO_PUBLIC_API_BASE_URL تنظیم شود
 * (فایل .env در ریشه‌ی mobile/، خوانده‌شده توسط Expo در زمان build).
 */
import { tokenStorage } from "./storage";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await tokenStorage.get();
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

export interface Project {
  id: string;
  name: string;
  location: string | null;
  is_archived: boolean;
}

export type DefectSeverity = "minor" | "major" | "critical";

export interface DefectCreate {
  project_id: string;
  contractor_name?: string | null;
  title: string;
  description: string;
  category?: string | null;
  location: string;
  photo_before_url?: string | null;
  voice_note_url?: string | null;
  gps_lat?: number | null;
  gps_lng?: number | null;
  floor_plan_x?: number | null;
  floor_plan_y?: number | null;
  severity: DefectSeverity;
}

export interface DefectOut extends DefectCreate {
  id: string;
  status: string;
  reopened_count: number;
}

export const api = {
  login: (email: string, password: string) =>
    apiFetch<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  getProjects: () => apiFetch<Project[]>("/projects"),
  reportDefect: (payload: DefectCreate) =>
    apiFetch<DefectOut>("/qa/defects", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
