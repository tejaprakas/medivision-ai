"use client";
import { Toaster } from "react-hot-toast";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
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
    </>
  );
}
