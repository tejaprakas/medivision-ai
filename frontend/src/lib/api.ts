// src/lib/api.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor — attach JWT token
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — handle 401
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

// Auth APIs
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', null, { params: { email, password } }),
  register: (data: { email: string; password: string; full_name: string; role: string }) =>
    api.post('/auth/register', data),
  refresh: (token: string) =>
    api.post('/auth/refresh', null, { params: { refresh_token: token } }),
  getMe: () => api.get('/auth/me'),
  verifyOTP: (email: string, otp: string) =>
    api.post('/auth/verify-otp', { email, otp_code: otp }),
  forgotPassword: (email: string) =>
    api.post('/auth/forgot-password', { email }),
  resetPassword: (token: string, newPassword: string) =>
    api.post('/auth/reset-password', { token, new_password: newPassword }),
};

// Analysis APIs
export const analysisAPI = {
  upload: (file: File, imageType: string) => {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('image_type', imageType);
    return api.post('/analysis/upload', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getResults: (skip = 0, limit = 20) =>
    api.get('/analysis/results', { params: { skip, limit } }),
  getDetail: (id: string) => api.get(`/analysis/results/${id}`),
  delete: (id: string) => api.delete(`/analysis/results/${id}`),
};

// Chatbot APIs
export const chatbotAPI = {
  createSession: (language = 'english') =>
    api.post('/chatbot/sessions', null, { params: { language } }),
  getSessions: () => api.get('/chatbot/sessions'),
  getMessages: (sessionId: string) =>
    api.get(`/chatbot/sessions/${sessionId}/messages`),
  sendMessage: (content: string, sessionId?: string, language = 'english') =>
    api.post('/chatbot/chat', { content, session_id: sessionId, language }),
  deleteSession: (sessionId: string) =>
    api.delete(`/chatbot/sessions/${sessionId}`),
};

// Reports APIs
export const reportsAPI = {
  generate: (analysisId: string) => api.post(`/reports/generate/${analysisId}`),
  getMyReports: () => api.get('/reports/my-reports'),
  download: (reportId: string) => api.get(`/reports/download/${reportId}`, { responseType: 'blob' }),
};

// Notifications APIs
export const notificationsAPI = {
  getAll: (unreadOnly = false) => api.get('/notifications', { params: { unread_only: unreadOnly } }),
  markRead: (id: string) => api.post(`/notifications/${id}/read`),
  markAllRead: () => api.post('/notifications/read-all'),
  getUnreadCount: () => api.get('/notifications/unread-count'),
};

// Analytics APIs
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getPatient: (patientId: string) => api.get(`/analytics/patient/${patientId}`),
};

// Appointments APIs
export const appointmentsAPI = {
  book: (data: { doctor_id: string; appointment_date: string; type?: string; reason?: string }) =>
    api.post('/appointments/book', data),
  getMy: (status?: string) => api.get('/appointments/my-appointments', { params: { status_filter: status } }),
  update: (id: string, data: { status?: string; notes?: string }) =>
    api.patch(`/appointments/${id}`, data),
};

// Doctors APIs
export const doctorsAPI = {
  list: (specialization?: string) => api.get('/doctors/list', { params: { specialization } }),
  getProfile: () => api.get('/doctors/profile'),
  updateProfile: (data: Record<string, unknown>) => api.put('/doctors/profile', data),
};

// Patients APIs
export const patientsAPI = {
  getProfile: () => api.get('/patients/profile'),
  updateProfile: (data: Record<string, unknown>) => api.put('/patients/profile', data),
};

// Admin APIs
export const adminAPI = {
  getUsers: (params?: Record<string, string>) => api.get('/admin/users', { params }),
  updateUserStatus: (userId: string, status: string) =>
    api.patch(`/admin/users/${userId}/status`, null, { params: { new_status: status } }),
  getStats: () => api.get('/admin/stats'),
};
