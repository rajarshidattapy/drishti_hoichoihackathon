import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Drishti — Semantic timeline",
  description: "Context intelligence and Bengali localization for every scene.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

