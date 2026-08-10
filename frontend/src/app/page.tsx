import Link from "next/link";

export default function HomePage() {
  return (
    <main className="container">
      <h1>Sakhtban — پنل کنترل پروژه</h1>
      <p style={{ color: "var(--muted)" }}>
        این پنل هنوز در مرحله‌ی اسکلت اولیه است. برای شروع باید وارد شوید یا شناسه‌ی پروژه را مستقیم در آدرس وارد کنید.
      </p>
      <Link href="/login" className="card" style={{ display: "inline-block", marginTop: 16 }}>
        ورود به حساب کاربری
      </Link>
    </main>
  );
}
