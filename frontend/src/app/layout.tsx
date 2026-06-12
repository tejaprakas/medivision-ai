import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MediVision AI - AI-Powered Heart Disease Detection",
  description: "Upload ECG, MRI, CT Scan or X-Ray images and receive intelligent AI-powered analysis, risk assessment, and medical explanations.",
  keywords: ["AI healthcare", "heart disease detection", "medical image analysis", "ECG analysis", "AI chatbot"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
