import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LuminaMed Patient Portal",
  description: "Understanding your radiology report, simplified",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
