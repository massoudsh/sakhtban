/**
 * صف آفلاین برای ثبت ایراد (issue #22 — «باید آفلاین‌فرست کار کند، اینترنت ضعیف کارگاه»).
 *
 * وقتی اتصال نیست یا درخواست شکست می‌خورد، آیتم (با URI محلی عکس/صدا) در AsyncStorage
 * صف می‌شود. با برگشت اتصال (NetInfo) یا فراخوانی دستی flushQueue، صف به‌ترتیب پردازش
 * می‌شود: هر آیتم ابتدا فایل‌های محلی (`file://...`) را به سرور آپلود می‌کند (`POST /uploads`)
 * و URL برگشتی را جایگزین می‌کند، سپس ایراد را با URLهای واقعی ثبت می‌کند. اگر آپلود هم
 * شکست بخورد (مثلاً هنوز آفلاین)، آیتم با URI محلی در صف می‌ماند تا تلاش بعدی.
 */
import AsyncStorage from "@react-native-async-storage/async-storage";
import NetInfo from "@react-native-community/netinfo";
import { api, uploadFile, type DefectCreate } from "./api";

/** فایل‌های محلی روی دستگاه هنوز آپلود نشده‌اند (`file://` است، نه URL سرور). */
function isLocalUri(uri: string | null | undefined): uri is string {
  return !!uri && (uri.startsWith("file://") || uri.startsWith("content://") || uri.startsWith("ph://"));
}

/** عکس/صدای محلی را آپلود می‌کند و آدرس سرور را جایگزین payload می‌کند. */
async function resolveLocalUploads(payload: DefectCreate): Promise<DefectCreate> {
  const resolved = { ...payload };
  if (isLocalUri(resolved.photo_before_url)) {
    const { url } = await uploadFile(resolved.project_id, resolved.photo_before_url, "photo");
    resolved.photo_before_url = url;
  }
  if (isLocalUri(resolved.voice_note_url)) {
    const { url } = await uploadFile(resolved.project_id, resolved.voice_note_url, "voice");
    resolved.voice_note_url = url;
  }
  return resolved;
}

/** آپلود فایل‌های محلی (در صورت وجود) + ثبت ایراد. برای ارسال فوری و flush صف مشترک است. */
async function sendDefect(payload: DefectCreate): Promise<void> {
  const resolved = await resolveLocalUploads(payload);
  await api.reportDefect(resolved);
}

const QUEUE_KEY = "sakhtban_defect_queue";

export interface QueuedDefect {
  localId: string;
  payload: DefectCreate;
  queuedAt: string;
  lastError?: string;
}

async function readQueue(): Promise<QueuedDefect[]> {
  const raw = await AsyncStorage.getItem(QUEUE_KEY);
  return raw ? (JSON.parse(raw) as QueuedDefect[]) : [];
}

async function writeQueue(queue: QueuedDefect[]): Promise<void> {
  await AsyncStorage.setItem(QUEUE_KEY, JSON.stringify(queue));
}

export async function enqueueDefect(payload: DefectCreate): Promise<QueuedDefect> {
  const queue = await readQueue();
  const item: QueuedDefect = {
    localId: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    payload,
    queuedAt: new Date().toISOString(),
  };
  queue.push(item);
  await writeQueue(queue);
  return item;
}

export async function getQueue(): Promise<QueuedDefect[]> {
  return readQueue();
}

/** تلاش برای ارسال «مستقیم»؛ اگر شکست خورد یا آفلاین بود، به صف اضافه می‌شود. */
export async function submitOrQueue(payload: DefectCreate): Promise<{ sentNow: boolean }> {
  const netState = await NetInfo.fetch();
  if (netState.isConnected && netState.isInternetReachable !== false) {
    try {
      await sendDefect(payload);
      return { sentNow: true };
    } catch {
      await enqueueDefect(payload);
      return { sentNow: false };
    }
  }
  await enqueueDefect(payload);
  return { sentNow: false };
}

/** خالی کردن صف — هر آیتمی که ارسالش موفق شود از صف حذف می‌شود، بقیه برای تلاش بعدی می‌مانند. */
export async function flushQueue(): Promise<{ sent: number; remaining: number }> {
  const queue = await readQueue();
  if (queue.length === 0) return { sent: 0, remaining: 0 };

  const stillQueued: QueuedDefect[] = [];
  let sent = 0;

  for (const item of queue) {
    try {
      await sendDefect(item.payload);
      sent += 1;
    } catch (err) {
      stillQueued.push({ ...item, lastError: err instanceof Error ? err.message : "خطای نامشخص" });
    }
  }

  await writeQueue(stillQueued);
  return { sent, remaining: stillQueued.length };
}

/** گوش‌دادن به برگشت اتصال برای flush خودکار — در App.tsx یک‌بار صدا زده می‌شود. */
export function subscribeAutoFlush(onFlushed?: (result: { sent: number; remaining: number }) => void): () => void {
  return NetInfo.addEventListener((state) => {
    if (state.isConnected && state.isInternetReachable !== false) {
      flushQueue().then((result) => {
        if (result.sent > 0) onFlushed?.(result);
      });
    }
  });
}
