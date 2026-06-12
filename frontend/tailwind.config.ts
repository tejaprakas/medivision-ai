@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 15, 23, 42;
  --background-start-rgb: 248, 250, 252;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 248, 250, 252;
    --background-start-rgb: 2, 6, 23;
    --background-end-rgb: 15, 23, 42;
  }
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

html {
  scroll-behavior: smooth;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
    to bottom,
    transparent,
    rgb(var(--background-end-rgb))
  )
  rgb(var(--background-start-rgb));
  font-family: var(--font-inter), system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

/* Selection */
::selection {
  background: rgba(37, 99, 235, 0.2);
  color: #1e293b;
}

/* Focus styles for accessibility */
*:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
  border-radius: 4px;
}

/* Smooth transitions for dark mode */
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
