import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "MediVision AI - AI-Powered Heart Disease Detection",
  description: "Upload ECG, MRI, CT Scan or X-Ray images and receive intelligent AI-powered analysis, risk assessment, and medical explanations.",
  keywords: ["AI healthcare", "heart disease detection", "medical image analysis", "ECG analysis", "AI chatbot"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
