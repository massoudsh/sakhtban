import type { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "Sakhtban — پنل کنترل پروژه",
  description: "کوپایلوت هوشمند کنترل پروژه‌های ساختمانی و عمرانی",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
