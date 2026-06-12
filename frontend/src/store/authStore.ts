// src/store/authStore.ts
import { create } from 'zustand';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'patient' | 'doctor' | 'admin';
  status: string;
  phone?: string;
  avatar_url?: string;
  email_verified: boolean;
}

interface AuthState {
  user: User | null;
  access_token: string | null;
  refresh_token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  setTokens: (access: string, refresh: string) => void;
  login: (user: User, access: string, refresh: string) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  access_token: typeof window !== 'undefined' ? localStorage.getItem('access_token') : null,
  refresh_token: typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null,
  isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('access_token') : false,
  isLoading: false,

  setUser: (user) => set({ user }),

  setTokens: (access, refresh) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
    }
    set({ access_token: access, refresh_token: refresh, isAuthenticated: true });
  },

  login: (user, access, refresh) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
    }
    set({ user, access_token: access, refresh_token: refresh, isAuthenticated: true });
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
    set({ user: null, access_token: null, refresh_token: null, isAuthenticated: false });
  },

  setLoading: (loading) => set({ isLoading: loading }),
}));
