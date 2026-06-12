"use client";

import { ThemeProvider } from "next-themes";
import { Toaster } from "react-hot-toast";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: "#1E293B",
            color: "#F8FAFC",
            borderRadius: "12px",
            fontSize: "14px",
          },
        }}
      />
    </ThemeProvider>
  );
}
