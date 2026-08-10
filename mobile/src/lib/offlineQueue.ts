/**
 * صف آفلاین برای ثبت ایراد (issue #22 — «باید آفلاین‌فرست کار کند، اینترنت ضعیف کارگاه»).
 *
 * وقتی اتصال نیست یا درخواست شکست می‌خورد، آیتم در AsyncStorage صف می‌شود.
 * با برگشت اتصال (NetInfo) یا فراخوانی دستی flushQueue، صف به‌ترتیب به API فرستاده می‌شود.
 *
 * نکته‌ی صادقانه: photo_before_url/voice_note_url در این مرحله همان URI محلی دستگاه
 * است (نه لینک عمومی روی object storage). آپلود واقعی فایل به S3/MinIO یک تصمیم
 * زیرساختی جداست که در specs/issue-22.md مستند شده و خارج از این تسک است.
 */
import AsyncStorage from "@react-native-async-storage/async-storage";
import NetInfo from "@react-native-community/netinfo";
import { api, type DefectCreate } from "./api";

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
      await api.reportDefect(payload);
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
      await api.reportDefect(item.payload);
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
