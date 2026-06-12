// src/types/index.ts
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'patient' | 'doctor' | 'admin';
  status: string;
  phone?: string;
  avatar_url?: string;
  email_verified: boolean;
  last_login?: string;
  created_at: string;
}

export interface PatientProfile {
  id: string;
  user_id: string;
  age?: number;
  gender?: string;
  blood_group?: string;
  height_cm?: number;
  weight_kg?: number;
  address?: string;
  city?: string;
  state?: string;
  country: string;
  health_score?: number;
  total_analyses: number;
  total_reports: number;
  allergies: Array<{ allergen: string; severity: string; notes?: string }>;
  current_medications: Array<{ name: string; dosage: string; frequency: string }>;
  medical_conditions: Array<{ condition: string; status: string; notes?: string }>;
}

export interface DoctorProfile {
  id: string;
  user_id: string;
  full_name: string;
  email: string;
  qualification?: string;
  specialization?: string;
  license_number?: string;
  hospital?: string;
  experience_years?: number;
  consultation_fee?: number;
  rating: number;
  total_reviews: number;
  total_patients: number;
  is_available: boolean;
}

export interface AnalysisResult {
  id: string;
  user_id: string;
  image_url: string;
  image_type: string;
  original_filename: string;
  prediction: string;
  disease_name?: string;
  confidence_score: number;
  risk_level: string;
  risk_score: number;
  detected_patterns: string[];
  findings: string[];
  recommendations: string[];
  ai_explanation?: string;
  status: string;
  processing_time_ms?: number;
  doctor_reviewed: boolean;
  report_generated: boolean;
  created_at: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export interface ChatSession {
  id: string;
  title?: string;
  language: string;
  is_active: boolean;
  message_count: number;
  created_at: string;
}

export interface MedicalReport {
  id: string;
  report_number: string;
  title: string;
  image_type: string;
  prediction: string;
  confidence_score: number;
  risk_level: string;
  pdf_url?: string;
  pdf_generated: boolean;
  created_at: string;
}

export interface Appointment {
  id: string;
  patient_id: string;
  doctor_id: string;
  appointment_date: string;
  duration_minutes: number;
  type: string;
  status: string;
  reason?: string;
  notes?: string;
  meeting_link?: string;
  created_at: string;
}

export interface Notification {
  id: string;
  type: string;
  priority: string;
  title: string;
  message: string;
  is_read: boolean;
  action_url?: string;
  created_at: string;
}

export interface DashboardAnalytics {
  users: { total: number; patients: number; doctors: number };
  analyses: { total: number; completed: number; pending: number; failed: number };
  risk_distribution: Record<string, number>;
  image_type_distribution: Record<string, number>;
  monthly_analyses: Array<{ date: string; count: number }>;
  appointments: { total: number; pending: number; completed: number };
  reports: { total: number };
}
